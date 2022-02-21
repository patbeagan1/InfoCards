package com.nani.aniscaper

import com.nani.aniscaper.Consts.WIKIPEDIA
import com.nani.aniscaper.datasource.WikiListOfFilmsRemoteDataSource
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val startTime = System.currentTimeMillis()
    WikiListOfFilmsRemoteDataSource(
        "$WIKIPEDIA/wiki/List_of_films_with_a_100%25_rating_on_Rotten_Tomatoes",
        Dispatchers.IO
    )
        .getMovies()
        ?.forEach { println(it) }
    println("${(System.currentTimeMillis() - startTime) / 1000} seconds")
}
