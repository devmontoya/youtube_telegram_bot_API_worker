from api.schemas.requests import Filter
from database.db_service import ClientChannelDb
from database.models.tables import ClientChannel


def get_new_channels_videos_for_client(session, client, channel):
    channel_id = channel.id
    list_videos = channel.videos
    last_id_video = list_videos[-1].id
    # Updating client-channel relationship
    client_channel_relationship = ClientChannelDb.get_element_with_double_filter(
        session,
        Filter(column="client_id", value=client.id),
        Filter(column="channel_id", value=channel_id),
    )
    if client_channel_relationship is None:
        new_client_channel = ClientChannel(
            client_id=client.id, channel_id=channel_id, last_id=last_id_video
        )
        ClientChannelDb.add_new_element(session, new_client_channel)
        num_new_videos = len(list_videos)
    else:
        # Compares the last video with the last one known for the user
        num_new_videos = channel.last_id - client_channel_relationship.last_id
        if num_new_videos > 0:
            list_videos = list_videos[-num_new_videos:]
            client_channel_relationship.last_id = channel.last_id
        else:
            list_videos = []
    session.flush()
    return num_new_videos, list_videos
