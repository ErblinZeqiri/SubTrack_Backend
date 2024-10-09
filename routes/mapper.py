from firebase_admin.firestore import DocumentReference, DocumentSnapshot

from .models import User, Subscription, Payment


# # # User Mapper # # #
class UserMapper:
  def to_user(self, user: dict | DocumentSnapshot | DocumentReference) -> User:
    user_dict = {}
    if isinstance(user, DocumentReference):
      user_dict.update({"uid" : user.id})
      user = user.get().to_dict()      
    elif isinstance(user, DocumentSnapshot):
      user_dict.update({"uid" : user.id})
      user = user.to_dict()

    user_dict.update(user)

    return User(
      user_dict.get("uid", ""),
      user_dict.get("email", ""),
      user_dict.get("fullName", ""),
      user_dict.get("password", ""),
      user_dict.get("salt", "")
    )
  
  def to_dict(self, user: User) -> dict:
    return {
      u"uid": user.uid,
      u"email": user.email,
      u"fullName": user.fullName,
      u"password": user.password,
      u"salt": user.salt
    }

  def to_firestore_dict(self, user: User) -> dict:
    return {
      u"uid": user.uid,
      u"email": user.email,
      u"fullName": user.fullName,
      u"password": user.password,
      u"salt": user.salt
    }
  
# # # Subscription Mapper # # #
class SubscriptionMapper:
  def to_subscription(self, subscription: dict | DocumentSnapshot | DocumentReference) -> Subscription:
      subscription_dict = {}
      if isinstance(subscription, DocumentReference):
          subscription_dict.update({"id": subscription.id})
          subscription = subscription.get().to_dict()
      elif isinstance(subscription, DocumentSnapshot):
          subscription_dict.update({"id": subscription.id})
          subscription = subscription.to_dict()

      subscription_dict.update(subscription)

      payment_history_data = subscription_dict.get("paymentHistory", [])
      payment_history = [
          Payment(payment.get("date", ""), payment.get("amount", 0))
          for payment in payment_history_data
      ]

      return Subscription(
          subscription_dict.get("id", ""),
          subscription_dict.get("companyName", ""),
          subscription_dict.get("nextPaymentDate", ""),
          subscription_dict.get("amount", 0),
          subscription_dict.get("category", ""),
          subscription_dict.get("renewal", ""),
          payment_history,
          subscription_dict.get("deadline", ""),
          subscription_dict.get("domain", ""),
          subscription_dict.get("logo", ""),
          subscription_dict.get("userID", "")
      )

  def to_dict(self, subscription: Subscription) -> dict:
      return {
          u"id": subscription.id,
          u"companyName": subscription.companyName,
          u"nextPaymentDate": subscription.nextPaymentDate,
          u"amount": subscription.amount,
          u"category": subscription.category,
          u"renewal": subscription.renewal,
          u"paymentHistory": [payment.to_dict() for payment in subscription.paymentHistory],
          u"deadline": subscription.deadline,
          u"domain": subscription.domain,
          u"logo": subscription.logo,
          u"userID": subscription.userID
      }


  def to_firestore_dict(self, subscription: Subscription) -> dict:
    print("Appel de to_firestore_dict")
    payment_history = [payment.to_dict() for payment in subscription.paymentHistory]
    if not payment_history:
        payment_history = []
    return {
        u"id": subscription.id, 
        u"companyName": subscription.companyName,
        u"nextPaymentDate": subscription.nextPaymentDate,
        u"amount": subscription.amount,
        u"category": subscription.category,
        u"renewal": subscription.renewal,
        u"paymentHistory": [payment.to_dict() for payment in subscription.paymentHistory],
        u"deadline": subscription.deadline,
        u"domain": subscription.domain,
        u"logo": subscription.logo,
        u"userID": subscription.userID
    }
    
class Payment:
  def __init__(self, date, amount):
      self.date = date
      self.amount = amount

  def to_dict(self):
      return {"date": self.date, "amount": self.amount}