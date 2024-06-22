from pydantic import BaseModel


# Look at the output example in README.md so you can see how the fields look like in the webpage.
class ClothUnit(BaseModel):
    # Url to the product
    product_url: list
    # Unique id number of the product. It can be found below the metadata section of the product.
    sku: str
    # The name that can be found in the webpage
    product_name: str
    # List of urls of all the images the product have
    images: list[str]
    # Composition, details about manufacturing, washing care, etc. This fields is kind of a bag of leftovers
    metadata: list[str]
    # The price of the product
    price: str
    # A list of the available sizes for the product
    sizes: list[str]
    # This field should contain what type of clothing it is (skirt, t-shirt, etc.)
    cloth_type: str
