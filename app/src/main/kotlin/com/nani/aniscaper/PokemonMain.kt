package com.nani.aniscaper

import kotlinx.coroutines.runBlocking
import org.jsoup.nodes.Element
import java.net.URL
import java.util.EmptyStackException
import java.util.Stack

fun main() = runBlocking {
    val startTime = System.currentTimeMillis()
    PokemonEvolutionDataSource().invoke()
    println("${(System.currentTimeMillis() - startTime) / 1000} seconds")
}

enum class PokemonType {
    FIRE,
    WATER,
    ELECTRIC,
    GRASS,
    NORMAL,
    DARK,
    BUG,
    PSYCHIC,
    POISON,
    GROUND,
    ROCK,
    DRAGON,
    FAIRY,
    FLYING,
    FIGHTING,
    ICE,
    STEEL,
    GHOST
}

data class Pokemon(
    val number: String?,
    val name: String?,
    val typePrimary: String?,
    val typeSecondary: String?,
    val imageUrl: URL
) : EvolutionElement

data class Evolution(
    val pokemonStart: Pokemon?,
    var pokemonEnd: Pokemon?,
    val condition: String?
) : EvolutionElement

class EvolutionSplit : EvolutionElement

interface EvolutionElement

class PokemonEvolutionDataSource : Scraper {
    private val link: String = "https://pokemondb.net/evolution"
    fun invoke() {
        println(link)
        getDocument(link)
            ?.body()
            ?.select("main > div.infocard-list-evo")
            ?.forEach { outerEvoList ->
                val items = outerEvoList.getElementsByClass("infocard")
                val containsSplit =
                    outerEvoList.getElementsByClass("infocard-evo-split").first()?.children()
                val evoStack = Stack<EvolutionElement>()

                if (containsSplit?.isNotEmpty() == true) {
                    containsSplit.forEach { evoSplitElement ->
                        val infoCards = evoSplitElement.getElementsByClass("infocard")
//                        val previousEvolution = evoStack.takeLastWhile { it !is EvolutionSplit }
                        evoStack.push(EvolutionSplit())
//                        previousEvolution.forEach { evoStack.push(it) }
                        evoStack.push(items.first()?.toPokemon())
                        infoCards.forEach {
                            checkPokemon(it, evoStack)
                            checkEvolution(it, evoStack)
                        }
                    }
                } else {
                    items.forEach { element ->
                        checkPokemon(element, evoStack)
                        checkEvolution(element, evoStack)
                    }
                }
                println(listOf(evoStack))
            }
    }

    private fun checkEvolution(
        element: Element,
        evoStack: Stack<EvolutionElement>
    ) {
        if (element.hasClass("infocard-arrow")) {
            val condition = element.getElementsByTag("small").text()
            if (evoStack.peekOrNull() is Pokemon) {
                evoStack.push(Evolution(evoStack.pop() as Pokemon, null, condition))
            }
        }
    }


//    [[com.nani.aniscaper.
//    EvolutionSplit@291b4bf5,
//    Evolution(pokemonStart=Pokemon(number=#172, name=Pichu, typePrimary=Electric, typeSecondary=null, imageUrl=https:), pokemonEnd=Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=null, imageUrl=https:), condition=(use Thunder Stone, outside Alola)),
//    Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=null, imageUrl=https:), com.nani.aniscaper.
//    EvolutionSplit@2d2ffcb7,
//    Evolution(pokemonStart=Pokemon(number=#172, name=Pichu, typePrimary=Electric, typeSecondary=null, imageUrl=https:), pokemonEnd=Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=Psychic, imageUrl=https:), condition=(use Thunder Stone, in Alola)),
//    Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=Psychic, imageUrl=https:)]]

//    [[com.nani.aniscaper.
//    EvolutionSplit@762ef0ea,
//    Evolution(pokemonStart=Pokemon(number=#043, name=Oddish, typePrimary=Grass, typeSecondary=Poison, imageUrl=https:), pokemonEnd=Pokemon(number=#045, name=Vileplume, typePrimary=Grass, typeSecondary=Poison, imageUrl=https:), condition=(use Leaf Stone)),
//    Pokemon(number=#045, name=Vileplume, typePrimary=Grass, typeSecondary=Poison, imageUrl=https:), com.nani.aniscaper.
//    EvolutionSplit@31f9b85e,
//    Evolution(pokemonStart=Pokemon(number=#043, name=Oddish, typePrimary=Grass, typeSecondary=Poison, imageUrl=https:), pokemonEnd=Pokemon(number=#182, name=Bellossom, typePrimary=Grass, typeSecondary=null, imageUrl=https:), condition=(use Sun Stone)),
//    Pokemon(number=#182, name=Bellossom, typePrimary=Grass, typeSecondary=null, imageUrl=https:)]]

//    [[com.nani.aniscaper.
//    EvolutionSplit@2d2ffcb7, Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=null, imageUrl=https:), com.nani.aniscaper.
//    EvolutionSplit@762ef0ea,
//    Evolution(pokemonStart=Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=null, imageUrl=https:), pokemonEnd=Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=Psychic, imageUrl=https:), condition=(use Thunder Stone, in Alola)), Pokemon(number=#026, name=Raichu, typePrimary=Electric, typeSecondary=Psychic, imageUrl=https:)]]

    private fun checkPokemon(
        element: Element,
        evoStack: Stack<EvolutionElement>
    ) {
        // we've found a pokemon
        if (element.children().hasClass("infocard-lg-img")) {
            val pokemon = element.toPokemon()
            val evolutionElement = evoStack.peekOrNull()
            if (evolutionElement is Evolution) {
                evolutionElement.pokemonEnd = pokemon
            }
            evoStack.push(pokemon)
        }
    }
}


private fun Stack<EvolutionElement>.peekOrNull() = try {
    peek()
} catch (e: EmptyStackException) {
    null
}

private fun Element.toPokemon(): Pokemon? {
    val types = getElementsByClass("itype").map { it.text() }
    return Pokemon(
        getElementsByTag("small").first()?.text(),
        getElementsByClass("ent-name").first()?.text(),
        types.first(),
        types.getOrNull(1),
        URL("https://" + getElementsByTag("img").attr("src"))
    )
}

