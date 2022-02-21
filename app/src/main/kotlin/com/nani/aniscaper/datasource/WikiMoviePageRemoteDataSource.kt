package com.nani.aniscaper.datasource

import com.nani.aniscaper.Scraper
import com.nani.aniscaper.model.Movie
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.jsoup.select.Elements

class WikiMoviePageRemoteDataSource(val link: String) : Scraper {
    fun extractMovieData(): Movie? {
        val doc: Document = getDocument(link) ?: return null
        val movieInfoBoxRows = doc.select(".infobox tr")

        return movieInfoBoxRows.fold(Movie()) { movie, ele ->
            val tagsTh: Elements = ele.getElementsByTag("th")
            val tagsImg = ele.getElementsByTag("img")
            when {
                tagsTh.hasClass("summary") -> movie.title = tagsTh.text()
                tagsImg.isNotEmpty() -> {
                    movie.posterURL = "https:" + tagsImg.attr("src")
                }
                else -> {
                    movie.extractMovieDataFromRow(ele, tagsTh)
                }
            }
            movie
        }
    }

    private fun Movie.extractMovieDataFromRow(
        ele: Element,
        tagsTh: Elements
    ) {
        val tagsLi = ele.getElementsByTag("li")
        val movieAttribute: String? = if (tagsLi.size > 1) {
            tagsLi
                .map(Element::text)
                .filter(String::isNotEmpty)
                .joinToString(", ")
        } else {
            ele.getElementsByTag("td")
                .first()
                ?.text()
        }
        when (tagsTh.first()?.text()?.lowercase()) {
            "directed by" -> directedBy = movieAttribute ?: ""
            "produced by" -> producedBy = movieAttribute ?: ""
            "written by" -> writtenBy = movieAttribute ?: ""
            "starring" -> starring = movieAttribute ?: ""
            "music by" -> musicBy = movieAttribute ?: ""
            "release date" -> releaseDate = movieAttribute ?: ""
            "running time" -> runningTime = movieAttribute ?: ""
            "title" -> title = movieAttribute ?: ""
        }
    }
}