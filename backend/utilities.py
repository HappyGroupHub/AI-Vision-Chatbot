import math
import os
import sys
from os.path import exists

from dotenv import load_dotenv


def env_file_generator():
    """Generate the template of config file"""
    with open('../.env', 'w', encoding="utf8") as file:
        file.write("""AI_VISION_KEY=
AI_VISION_ENDPOINT=
AOAI_KEY=
AOAI_ENDPOINT=
"""
                   )
        file.close()
    sys.exit()


def read_env():
    """Read config file.

    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.

    :rtype: dict
    """
    if not exists('../.env'):
        print("Environment file not found, create one by default.\nPlease finish filling .env")
        env_file_generator()

    try:
        load_dotenv('../.env')
        env = {'ai_vision_key': os.getenv('AI_VISION_KEY'),
               'ai_vision_endpoint': os.getenv('AI_VISION_ENDPOINT'),
               'aoai_key': os.getenv('AOAI_KEY'),
               'aoai_endpoint': os.getenv('AOAI_ENDPOINT')}
        return env
    except (KeyError, TypeError):
        print(
            "An error occurred while reading .env, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def get_cosine_similarity(vector1, vector2):
    """Get the cosine similarity between two vectors.

    :param list vector1: Vector 1
    :param list vector2: Vector 2
    :return float cosine_similarity: Cosine similarity
    """
    dot_product = 0
    length = min(len(vector1), len(vector2))

    for i in range(length):
        dot_product += vector1[i] * vector2[i]

    magnitude1 = math.sqrt(sum(x * x for x in vector1))
    magnitude2 = math.sqrt(sum(x * x for x in vector2))

    return dot_product / (magnitude1 * magnitude2)


def get_top_n_similar_images(target_vector, imageset_vector, n=3):
    """Get top n similar images from imageset.

    :param list target_vector: Given vector, can be image vector or text vector
    :param list imageset_vector: Imageset vector
    :param int n: Number of similar images, default is 3
    :return list top_n_similar_images: Top n similar images
    """
    similarity_dict = {}
    for image in imageset_vector:
        similarity = get_cosine_similarity(target_vector, imageset_vector[image])
        similarity_dict[image] = similarity
    top_n_similar_images = sorted(similarity_dict.items(), key=lambda x: x[1], reverse=True)[:n]
    return top_n_similar_images
