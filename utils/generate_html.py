import re
import markdown

from models import (
    tag as tag_model,
    recipe as recipe_model
)

def generate_slug(string: str):
    string = string.lower()
    string = re.sub(r'[^a-z0-9\s-]', '', string)
    string = re.sub(r'[\s-]+', '-', string).strip('-')

    return string

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

def generate_recipes(recipes: list[recipe_model.Recipe]):
    gen_html = ""

    if (len(recipes) > 0):

        for recipe in recipes:
            slug = generate_slug(recipe.name)
            gen_html += f"""
                <div class="cell">
                    <div class="card">
                        <div class="card-image">
                            <figure class="image is-4by3">
                            <img
                                style="object-fit: cover"
                                src="/static/img/{slug}.jpg"
                                alt="Placeholder image"
                            />
                            </figure>
                        </div>
                        <div class="card-content">
                            <div class="media">
                            <div class="media-content">
                                <p class="title is-4">{recipe.name}</p>
                                <p class="subtitle is-6"><span class="tag is-warning">{recipe.tag.name}</span></p>
                            </div>
                            </div>

                            <div class="content" style="overflow: scroll; max-height: 8rem" >
                            <nav class="level">
                                <div class="level-item">
                                    <span class="title is-7">{recipe.servings} SERVINGS</span>
                                </div>
                                <div class="level-item">
                                    <span class="title is-7">{recipe.calories} CALORIES</span>
                                </div>
                                <div class="level-item">
                                    <span class="title is-7">{recipe.protein}g PROTEIN</span>
                                </div>
                            </nav>
                            <br />
                            </div>
                            
                            <nav class="level">
                                <div class="level-item">
                                    <a href="/view-recipe.htm?id={recipe.id}">
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
                    alt="Placeholder image"
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
                    <nav class="level">
                        <div class="level-item">
                            <span class="title is-6">{recipe.servings} SERVINGS</span>
                        </div>
                        <div class="level-item">
                            <span class="title is-6">{recipe.calories} CALORIES</span>
                        </div>
                        <div class="level-item">
                            <span class="title is-6">{recipe.protein}g PROTEIN</span>
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
                </div>
            </div>
        </div>
    """
    return gen_html