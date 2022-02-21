package com.nani.aniscaper

import org.jsoup.Jsoup
import org.jsoup.nodes.Document

interface Scraper {
    fun getDocument(url: String): Document? = try {
        Jsoup.connect(url).get()
    } catch (e: Exception) {
        null
    }
}