import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from firebase_admin.firestore import DocumentSnapshot

from config.firestore_db import db

from .models import User, Subscription
from .mapper import UserMapper, SubscriptionMapper
from flask import g


class UserRepository:
  def __init__(self) -> None:
    self.collection = db.collection(u"users")
    self.mapper = UserMapper()
  
  def get_one(self, userID: str) -> User:
    user = self.collection.document(userID).get()

    if not user.exists:
      raise ValueError(f"user with uid {userID} doesn't exists")
    
    return self.mapper.to_user(user)
  
  def create_user(self, user: User) -> User:
    _, user_ref = self.collection.add(self.mapper.to_firestore_dict(user))
    user_snapshot = user_ref.get()
    user_dict = self.mapper.to_dict(user)
    user_dict['uid'] = user_snapshot.id
    user_ref.update(user_dict)
    return self.mapper.to_user(user_dict)

  def get_user_by_email(self, email: str) -> list[User]:
    return [self.mapper.to_user(d) for d in self.collection.where("email", "==", email).get()]
  

# # # Subscriptions # # #
class SubscriptionRepository:
  def __init__(self) -> None:
    self.collection = db.collection(u"subscriptions")
    self.mapper = SubscriptionMapper()

  def get_all(self, userID: str) -> list[Subscription]:
      subscriptions = self.collection.where("userID", "==", userID).get()
      
      valid_subscriptions = []
      for doc in subscriptions:
          subscription_data = doc.to_dict()
          if "userID" not in subscription_data or not isinstance(subscription_data["userID"], str):
              continue  # Ignorer les abonnements invalides ou mal formés
          valid_subscriptions.append(self.mapper.to_subscription(subscription_data))
      
      return valid_subscriptions

  def get_one(self, subscription_id: str) -> Subscription:
    subscription = self.collection.document(subscription_id).get()

    if not subscription.exists:
      raise ValueError(f"subscription with uid {subscription_id} doesn't exists")
    
    return self.mapper.to_subscription(subscription)
  
  def create_subscription(self, subscription: Subscription) -> Subscription:
    _, subscription_ref = self.collection.add(self.mapper.to_firestore_dict(subscription))
    subscription.id = subscription_ref.id
    subscription_ref.update({'id': subscription.id})
    # if subscription.userID == '':
    #   subscription.userID = g.userID
    #   subscription_ref.update({'userID': subscription.userID})
    return subscription

  def update_subscription(self, subscription: Subscription) -> Subscription:
    self.collection.document(subscription.id).set(self.mapper.to_firestore_dict(subscription))
    return subscription
  
  def delete_subscription(self, subscription_id: str) -> None:
    self.collection.document(subscription_id).delete()

  def get_filtered_subscriptions(self, userID: str, category: str, renewal: str) -> list[Subscription]:

    query = self.collection.where("userID", "==", userID)

    if category != 'Tout':
        query = query.where("category", "==", category)
    if renewal != 'Tout':
        query = query.where("renewal", "==", renewal)

    documents = query.get()
    subscriptions = []
    for doc in documents:
        subscription_data = doc.to_dict()
        subscriptions.append(subscription_data)

    return subscriptions