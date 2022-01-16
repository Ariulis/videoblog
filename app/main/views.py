from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import use_kwargs, marshal_with

from . import main
from .. import db, logger, docs
from ..models import Video
from ..schemas import VideoSchema
from ..base_view import BaseView


class VideosListView(BaseView):
    @marshal_with(VideoSchema(many=True))
    def get(self):
        try:
            videos = Video.get_list()
        except Exception as e:
            logger.warning(
                f'videos: get action failed with errors: {e}')
            return {
                'message': str(e)
            }, 400
        return videos


@main.route('/tutorials')
@jwt_required()
@marshal_with(VideoSchema(many=True))
@logger.catch
def get_list():
    try:
        author_id = get_jwt_identity()
        videos = Video.get_user_list(author_id)
    except Exception as e:
        logger.warning(
            f'user: {author_id} tutorials - read action failed with errors: {e}')
        return {
            'message': str(e)
        }, 400
    return videos


@main.route('/tutorials', methods=['POST'])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema())
@logger.catch
def add_item(**kwargs):
    try:
        author_id = get_jwt_identity()
        video = Video(author_id=author_id, **kwargs)
        video.save()
    except Exception as e:
        logger.warning(
            f'user: {author_id} tutorials - create action failed with errors: {e}')
        return {
            'message': str(e)
        }, 400
    return video


@main.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema())
@logger.catch
def update_list(tutorial_id, **kwargs):
    try:
        author_id = get_jwt_identity()
        video = Video.get(tutorial_id, author_id)
        video.update(**kwargs)
        video.save()
    except Exception as e:
        logger.warning(
            f'user: {author_id} tutorial: {tutorial_id} - update action failed with errors: {e}')
        return {
            'message': str(e)
        }, 400
    return video


@main.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required()
@marshal_with(VideoSchema)
@logger.catch
def delete_item(tutorial_id):
    author_id = get_jwt_identity()
    video = Video.get(tutorial_id, author_id)
    db.session.delete(video)
    try:
        db.session.commit()
    except Exception as e:
        logger.warning(
            f'user: {author_id} tutorial: {tutorial_id} - delete action failed with errors: {e}')
        return {
            'message': str(e)
        }, 400
    return '', 204


docs.register(get_list, blueprint="main")
docs.register(add_item, blueprint="main")
docs.register(update_list, blueprint="main")
docs.register(delete_item, blueprint="main")

VideosListView.register(main, docs, '/videos', 'videoslistview')
