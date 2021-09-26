import re

from django.db.models import Q


def generate_filter_for_posts(word):
    db_filter = Q(title__icontains=word) | Q(body__icontains=word) | \
                Q(user__name__icontains=word) | Q(user__username__icontains=word)

    try:
        db_filter |= Q(pk=int(word))
    except ValueError:
        pass

    return db_filter


def get_db_filter_based_on_search_query(search_query: str):
    db_filter = None
    cleaned_search_query = re.sub(r'[!\'()|&;,]', ' ', search_query).strip()

    if cleaned_search_query:
        words = cleaned_search_query.split()
        db_filter = generate_filter_for_posts(words[0])

        for word in words[1:]:
            db_filter &= generate_filter_for_posts(word)

    return db_filter
