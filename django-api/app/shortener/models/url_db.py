import uuid, string
from django.db import models
from django.conf import settings
from pymongo import ReturnDocument

# MongoDB collections
url_counter_collection = settings.MONGO_DB['url_counters']
reusable_shortcodes_collection = settings.MONGO_DB['reusable_shortcodes']


class ShortenedURL(models.Model):
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='urls')
    original_url = models.URLField(max_length=500, unique=True)
    short_code = models.CharField(max_length=50, unique=True, primary_key=True,)
    secret_key = models.UUIDField(editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_code


def base36_encode(number):
    """Encodes an integer in base-36."""
    assert number >= 0, 'Number must be non-negative'
    base36_chars = 'zyxwvZYXWVutsrqUTSRQponmlPONMLkjihgKJIHGfedcbFa'
    if number == 0:
        return base36_chars[0]
    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = base36_chars[i] + base36
    return base36_chars[-1] * (6 - len(base36)) + base36  # Ensures fixed 6-character length


def generate_unique_shortcode():
    """Generate a unique short code using MongoDB."""
    
    # Check if there are reusable shortcodes available in MongoDB
    reusable_code = reusable_shortcodes_collection.find_one()
    if reusable_code:
        short_code = reusable_code['short_code']
        reusable_shortcodes_collection.delete_one({'short_code': short_code})
        return short_code

    # If no reusable shortcode, use the counter in MongoDB
    result = url_counter_collection.find_one_and_update(
        {'_id': 'url_counter'},
        {'$inc': {'current_value': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    next_value = result['current_value']

    # Convert the counter value to base-36
    return base36_encode(next_value)


def store_reusable_shortcode(short_code):
    """Store deleted shortcodes in MongoDB for reuse."""
    reusable_shortcodes_collection.insert_one({'short_code': short_code})
