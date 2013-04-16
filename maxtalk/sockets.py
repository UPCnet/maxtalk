from pyramid.view import view_config
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin
from pyramid.httpexceptions import HTTPOk

from max.models import User


class NamedUsersRoomsMixin(BroadcastMixin):
    def __init__(self, *args, **kwargs):
        super(NamedUsersRoomsMixin, self).__init__(*args, **kwargs)

    def join(self, username):
        """Lets a user join a room on a specific Namespace."""
        user = User()
        user.request = self.request
        user.mdb_collection = self.request.db.users
        user.fromDatabase(username)
        subscribed_conversations = [a['id'] for a in user.talkingIn['items'] if a['objectType'] == 'conversation']
        self.socket.rooms = set(subscribed_conversations)
        print 'User %s listening to conversations: %s' % (username, ', '.join(subscribed_conversations))

    def leave(self, room):
        """Lets a user leave a room on a specific Namespace."""
        self.socket.rooms.remove(self._get_room_name(room))

    def _get_room_name(self, room):
        return self.ns_name + '_' + room

    def emit_to_room(self, event, args):
        """This is sent to all in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=(args,),
                   endpoint=self.ns_name)
        room_name = args['conversation']
        for sessid, socket in self.socket.server.sockets.iteritems():
            if self.socket != socket:
                if not hasattr(socket, 'rooms'):
                    continue
                if room_name in socket.rooms:
                    socket.send_packet(pkt)


class ConversationsNamespace(BaseNamespace, NamedUsersRoomsMixin):
    def on_chat(self, msg):
        self.emit_to_room('chat', msg)

    def recv_connect(self):
        self.broadcast_event('user_connect')

    def recv_disconnect(self):
        self.broadcast_event('user_disconnect')
        self.disconnect(silent=True)

    def on_join(self, channel):
        self.join(channel)


nsmap = {'/max': ConversationsNamespace}


@view_config(route_name='socket.io')
def socketio_service(request):
    """ The view that will launch the socketio listener """

    socketio_manage(request.environ, namespaces=nsmap, request=request)

    return HTTPOk()
