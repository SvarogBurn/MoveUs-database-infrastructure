"""
Database router for primary-replica setup
Routes reads to replicas, writes to primary
"""
import random


class PrimaryReplicaRouter:
    """
    A router to control database operations on Primary-Replica architecture
    
    - All writes go to 'default' (primary)
    - All reads are load-balanced between 'replica1' and 'replica2'
    - Migrations only run on 'default'
    """
    
    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly selected replica
        This provides load balancing across read replicas
        """
        return random.choice(['replica1', 'replica2'])
    
    def db_for_write(self, model, **hints):
        """
        Writes always go to primary
        """
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database
        Since all databases have the same schema, allow all relations
        """
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure migrations only run on the primary database
        """
        return db == 'default'