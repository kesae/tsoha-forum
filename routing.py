import routes.before_requests
import routes.board
import routes.filters
import routes.group
import routes.index
import routes.membership
import routes.post
import routes.session
import routes.topic
import routes.user

blueprints = [
    routes.before_requests.bp,
    routes.board.bp,
    routes.filters.bp,
    routes.group.bp,
    routes.index.bp,
    routes.membership.bp,
    routes.post.bp,
    routes.session.bp,
    routes.topic.bp,
    routes.user.bp,
]
