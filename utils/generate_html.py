import re
import markdown

from models import (
    tag as tag_model,
    cuisine as cuisine_model,
    recipe as recipe_model,
    review as review_model
)

def generate_slug(string: str):
    string = string.lower()
    string = re.sub(r'[^a-z0-9\s-]', '', string)
    string = re.sub(r'[\s-]+', '-', string).strip('-')

    return string

def generate_stars(rating: int):
    gen_html = ""

    for i in range(rating):
        gen_html += f"""
            <span key={i} className="icon">
                <i class="fa-solid fa-star" style="color: gold;"></i>
                </span>
            """
    
    return gen_html

def generate_markdown(string: str):
    return markdown.markdown(string, extensions=['tables'])

def generate_tags(tags: list[tag_model.Tag]):
    gen_html = """
        <option value="all" selected>Select Filter</option>
    """

    for tag in tags:
        gen_html += f"""
            <option value={tag.id}>{tag.name}</option>
        """

    return gen_html

def generate_cuisines(cuisines: list[cuisine_model.Cuisine]):
    gen_html = """
        <option value="all" selected>Select Filter</option>
    """

    for cuisine in cuisines:
        gen_html += f"""
            <option value={cuisine.id}>{cuisine.name}</option>
        """
    
    return gen_html

def generate_recipes(recipes: list[recipe_model.Recipe]):
    gen_html = ""

    if (len(recipes) > 0):

        for recipe in recipes:
            slug = generate_slug(recipe.name)
            gen_html += f"""
                <div class="cell">
                    <div class="card" style="height: 100%;">
                        <div class="card-image">
                            <figure class="image is-4by3">
                            <img
                                style="object-fit: cover"
                                src="/static/img/{slug}.jpg"
                                onerror="this.src='/static/img/image-not-found.jpg'"
                                alt="{recipe.name} image"
                            />
                            </figure>
                        </div>
                        <div class="card-content">
                            <div class="media">
                            <div class="media-content" style="min-height: 5rem">
                                <p class="title is-4">{recipe.name}</p>
                                <p class="subtitle is-6"><span class="tag is-warning">{recipe.tag.name}</span></p>
                            </div>
                            </div>

                            <div class="content" style="max-height: 8rem; min-height: 6rem;" >
                            <nav class="level is-mobile">
                                <div class="level-item has-text-centered">
                                    <div>
                                        <p class="title is-5">{recipe.servings}</p>
                                        <p class="title is-6">SERVINGS</p>
                                    </div>
                                </div>
                                <div class="level-item has-text-centered">
                                    <div>
                                        <p class="title is-5">{recipe.calories}</p>
                                        <p class="title is-6">CALORIES</p>
                                    </div>
                                </div>
                                <div class="level-item has-text-centered">
                                    <div>
                                        <p class="title is-5">{recipe.protein}g</p>
                                        <p class="title is-6">PROTEIN</p>
                                    </div>
                                </div>
                            </nav>
                            <br />
                            </div>
                            
                            <nav class="level">
                                <div class="level-item">
                                    <a href="/view-recipe.htm?id={recipe.id}&name={recipe.name}">
                                        <button class="button is-primary">View Recipe</button>
                                    </a>
                                </div>
                            </nav>
                        </div>
                    </div>
                </div>
            """

        return gen_html

    return gen_html

def generate_reviews(reviews: list[review_model.Review]):
    gen_html = ""
    
    if (len(reviews) > 0):
        
        for review in reviews:
            slug = generate_slug(review.name)
            if review.rating:
                rating = generate_stars(review.rating)
            else: rating = ""

            if review.visited:
                text = """
                <div class="icon-text">
                    <span class="title is-6">
                        <span key={i} class="icon has-text-primary">
                            <i class="fa-solid fa-check"></i>
                        </span>
                    </span>
                </div>
                """
            else:
                text = """
                <div class="icon-text">
                    
                    <span class="title is-6">
                        <span key={i} class="icon has-text-danger">
                            <i class="fa-solid fa-ban"></i>
                        </span>
                    </span>
                </div>
                """
            
            gen_html += f"""
                <div class="cell">
                    <div class="card" style="height: 100%;">
                        <div class="card-header">
                            <div class="card-header-title">
                                <p class="title is-4">{review.name}</p>
                            </div>
                            <div class="card-header-icon">
                                    <div>
                                        {text}
                                    </div>
                            </div>
                        </div>
                        <div class="card-content">
                            <div class="content" min-height: 6rem;" >
                                <div class="has-text-centered">
                                    <div>
                                        {rating}
                                    </div>
                                </div>
                                <nav class="level">
                                    <div class="level-item has-text-centered">
                                        <div>
                                            <p class="title is-6">{review.address}</p>
                                        </div>
                                    </div>
                                </nav>
                                <div class="has-text-centered">
                                    <span class="tag is-primary"><span class="title is-6">{review.cuisine.name.capitalize()}</span></span>
                                </div>
                            <br />
                            <p>
                                {review.notes}
                            </p>
                            </div>
                        </div>
                    </div>
                </div>
            """

    return gen_html

def generate_error_html():
    return """
    <article class="message is-danger">
        <div class="message-header">
            <p>Error</p>
        </div>
        <div class="message-body">
            There was a problem getting this recipe, or this recipe does not exist.
        </div>
    </article>
    """


def generate_recipe(recipe: recipe_model.Recipe):
    slug = generate_slug(recipe.name)
    ingredients = generate_markdown(recipe.ingredients)
    instructions = generate_markdown(recipe.instructions)

    gen_html = f"""
        <div class="card" style="margin: 0rem 1rem" >
            <div class="card-image">
                <figure class="image is-4by3">
                <img
                    style="object-fit: cover"
                    src="/static/img/{slug}.jpg"
                    onerror="this.src='/static/img/image-not-found.jpg'"
                    alt="{recipe.name} image"
                />
                </figure>
            </div>
            <div class="card-header">
                <div class="card-header-title">
                    <p class="title is-4">{recipe.name}</p>
                </div>
                <div class="card-header-icon">
                    <span class="tag is-warning">{recipe.tag.name}</span>
                </div>
            </div>
            <div class="card-content">
                <div class="content">
                    <nav class="level is-mobile">
                        <div class="level-item has-text-centered">
                                    <div>
                                        <p class="title is-5">{recipe.servings}</p>
                                        <p class="title is-6">SERVINGS</p>
                                    </div>
                                </div>
                                <div class="level-item has-text-centered">
                                    <div>
                                        <p class="title is-5">{recipe.calories}</p>
                                        <p class="title is-6">CALORIES</p>
                                    </div>
                                </div>
                                <div class="level-item has-text-centered">
                                    <div>
                                        <p class="title is-5">{recipe.protein}g</p>
                                        <p class="title is-6">PROTEIN</p>
                                    </div>
                                </div>
                    </nav>
                    <br />
                    <div class="columns is-centered">
                        <div class="column is-narrow">
                        <span class="title is-6">Ingredients</span>
                        <br />
                        <br />
                        {ingredients}
                        </div>
                        <div class="column is-two-thirds">
                        <span class="title is-6">Instructions</span>
                        <br />
                        <br />
                        {instructions}
                        </div>
                    </div>
                    <br />
                    <nav class="level">
                        <div class="level-item">
                            <button class="button is-primary" id="share-button" onClick="shareRecipe('{recipe.name}')">Share Recipe</button>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    """
    return gen_html