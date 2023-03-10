from flask_restx import Namespace,  Resource,fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import db

order_namespace = Namespace('orders', description= ' a name space for order')

order_model = order_namespace.model(
  'Orders', {
    'id' : fields.Integer(description= 'An ID'),
    'size': fields.String(description = 'Size of an Order', required = True, 
    enum = ['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']
    ),
    'order_status' : fields.String(description = 'Status of an order', required =True, 
    enum = ['PENDING', 'IN_TRANSIT','DELIVERED']
    ),
    'flavour': fields.String(description='flavour of the pizza', required=True),
    'quantity': fields.Integer(description= 'quantity of pizza', required= True)
  }
)

order_status_model =order_namespace.model(
  'OrderStatus', {
  'order_status': fields.String(required = True, description ='the status of our order',
                                    enum = ['PENDING', 'IN_TRANSIT','DELIVERED'])
  }
)


@order_namespace.route('/orders')
class OrderGetCreate(Resource):
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(
    description="Get All Orders"
  )
  @jwt_required()
  def get(self):
    """
      Get all Orders
    """
    orders = Order.query.all()

    return orders,  HTTPStatus.OK

  @order_namespace.expect(order_model)
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(
    description="Place An Order"
  )
  @jwt_required()
  def post(self):
    """
     Place all orders
    """
    username = get_jwt_identity()

    current_user = User.query.filter_by(username=username ).first()

    data = order_namespace.payload

    new_order = Order(
      size = data['size'],
      quantity = data['quantity'],
      flavour = data['flavour']
    )

    new_order.user = current_user

    new_order.save()

    return new_order, HTTPStatus.CREATED


@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):

  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(
    description="Get  Orders by Id",
    params = {
    'order_id' : 'An ID for an order'
    }
  )
  @jwt_required()
  def get(self,order_id):
    """
      Retrieving an order by id
    """
    order = Order.get_by_id(order_id)

    return order, HTTPStatus.OK

  @order_namespace.expect(order_model)
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(
    description="Update  Orders by Id",
    params = {
    'order_id' : 'An ID for an order'
    }
  )
  @jwt_required
  def put(self,order_id):
    """
      Update order by id
    """
    order_to_update = Order.get_by_id(order_id)

    data = order_namespace.payload

    order_to_update.quantity = data["quantity"]
    order_to_update.size = data["size"]
    order_to_update.flavour = data["flavour"]

    db.session.commit()

    return order_to_update, HTTPStatus.OK
  @order_namespace.doc(
    description="Delete an Order",
    params = {
    'order_id' : 'An ID for an order'
    }
  )
  @jwt_required
  def delete(self, order_id):
    """
      Delete order by id 
   """
    order_to_delete = Order.get_by_id(order_id)

    order_to_delete.delete()

    return {'message': 'order deleted successfully'}, HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderById(Resource):
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(
    description="Get a specific user order by id",
    params = {
    'order_id' : 'An ID for an order',
    'user_id' : 'An ID for a user'
    }
  )
  @jwt_required()
  def get(self, user_id,order_id):

    """
      Get a specific User order
    """
    user = User.get_by_id(user_id)

    order = Order.query.filter_by(id=order_id).filter_by(user=user).first()

    return order, HTTPStatus.OK




@order_namespace.route('/user/<int:user_id>/orders')
class UsersOrders(Resource):
  @order_namespace.marshal_list_with(order_model)
  @order_namespace.doc(
    description="Get all order by a user"
  )
  @jwt_required()
  def get(self, user_id):

    """
      Get all user orders
    """
    user = User.query.get_by_id(user_id)
    
    orders = user.orders
    
    return orders, HTTPStatus.OK

@order_namespace.route('/users/status/<int:order_id>')
class UpdateOrderStatus(Resource):
  @order_namespace.expect(order_status_model)
  @order_namespace.marshal_with(order_model)
  @order_namespace.doc(
    description="Update an order status",
    params = {
    'order_id' : 'An ID for an order'
    }
  )
  def patch(self,order_id):
    """
      Update an order status
    """
    data = order_namespace.payload

    order_to_update= Order.get_by_id(order_id)

    order_to_update.order_status = data["order_status"]

    db.session.commit()

    return order_to_update, HTTPStatus.OK
 



