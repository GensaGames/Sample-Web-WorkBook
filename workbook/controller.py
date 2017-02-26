import os

from webworkbook import settings


# Generate static Stories from the folder with all sources
# USE UNICODE METHOD, which missing on Python >= 3.5
# noinspection PyCompatibility
def generate_stories():
    stories_main_dir = os.path.join(settings.STATICFILES_DIRS[0], 'workbook', 'stories')
    stories_list = list()
    # Iterate all static folder for Articles and Stories
    for parent_file in os.listdir(stories_main_dir):
        story_dir = os.path.join(stories_main_dir, parent_file)
        story_img_source = story_text_source = story_header = story_html = None
        if not os.path.isdir(story_dir):
            continue
        # Gather all items, from Stories, like Tittle, Text and Img.
        for story_file in os.listdir(story_dir):
            story_iter_type = os.path.splitext(story_file)
            if story_iter_type[1] == '.html':
                story_html = os.path.join(story_dir, story_file)
                story_html = story_html.replace(os.path.join(settings.STATICFILES_DIRS[0], 'workbook', ''), '')
            if story_iter_type[1] == '.jpg':
                story_img_source = os.path.join(story_dir, story_file)
                story_img_source = story_img_source.replace(settings.BASE_DIR, '')
            if story_iter_type[1] == '.txt':
                with open(os.path.join(story_dir, story_file), 'r') as story:
                    story_text_source = unicode(story.read(), errors='ignore')
                    story_header = story_iter_type[0]
        # Using list of tuples this items and transfer.
        if story_header is not None and story_text_source is not None \
                and story_img_source is not None and story_html is not None:
            stories_list.append((story_html, story_header, story_text_source, story_img_source))
    return stories_list

STATIC_STORIES = generate_stories()
