package com.nani.aniscaper.datasource

import com.nani.aniscaper.Consts.WIKIPEDIA
import com.nani.aniscaper.Scraper
import com.nani.aniscaper.model.Movie
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext

class WikiListOfFilmsRemoteDataSource(
    private val wikiLinkUrl: String,
    private val coroutineDispatcher: CoroutineDispatcher
) : Scraper {

    suspend fun getMovies(): List<Movie?>? {
        val doc = getDocument(wikiLinkUrl) ?: return null

        return withContext(coroutineDispatcher) {
            val wikiTable = doc.select(".wikitable:first-of-type tr td:first-of-type a")
            wikiTable
                .map {
                    val link = it.attr("href")
                    WikiMoviePageRemoteDataSource(WIKIPEDIA + link)
                }
                .mapIndexed { index, each ->
                    async {
                        rateLimit(index, wikiTable.size, each)
                        each.extractMovieData()
                    }
                }
                .awaitAll()
                .filterNotNull()
        }
    }

    private suspend fun rateLimit(
        index: Int,
        length: Int,
        each: WikiMoviePageRemoteDataSource
    ) {
        delay((index * 100).toLong())
        val percentComplete = (100.0 * index.toDouble() / length.toDouble()).toInt()
        println("Visiting: $percentComplete% ${each.link}")
    }
}
