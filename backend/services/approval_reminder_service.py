"""
Approval Reminder Service

This service identifies pending ECO approvals for the current stage
and sends periodic notifications to the respective approvers.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.core.database import SessionLocal
from backend.models.plm_eco_approval import EcoApproval
from backend.models.plm_eco import Eco
from backend.services.notification_service import get_notification_service

logger = logging.getLogger(__name__)


class ApprovalReminderService:
    """Service to send reminders to users with pending approvals."""
    
    def __init__(self, db: Optional[Session] = None):
        """
        Initialize the service.
        
        Args:
            db: Database session. If None, a new session is created.
        """
        self._provided_db = db
        self._notification_service = None

    def _get_db(self) -> Session:
        return self._provided_db if self._provided_db else SessionLocal()

    def _get_notification_service(self, db: Session):
        if self._notification_service is None:
            self._notification_service = get_notification_service(db)
        return self._notification_service

    def run_reminders(self) -> Dict[str, Any]:
        """
        Scan for pending approvals in the current stage of each ECO and send notifications.
        
        Returns:
            Dict containing success status and number of reminders sent.
        """
        start_time = datetime.utcnow()
        logger.info("Starting ECO approval reminder process")
        
        db = self._get_db()
        try:
            # Join EcoApproval with Eco to ensure we only remind for the *current* stage
            # EcoApproval records are created per stage, but we only care about the one
            # matching the ECO's current stage_id.
            pending_approvals = db.query(EcoApproval).join(
                Eco, Eco.id == EcoApproval.eco_id
            ).filter(
                and_(
                    EcoApproval.approved == False,
                    Eco.stage_id == EcoApproval.stage_id
                )
            ).all()

            sent_count = 0
            notification_service = self._get_notification_service(db)
            
            for approval in pending_approvals:
                try:
                    # In ZnovaModel, ECOApproval.user_id returns the actual User recordset due to Many2one override
                    # ECOApproval.eco_id returns the Eco recordset
                    # ECOApproval.stage_id returns the Stage recordset
                    
                    user = approval.user_id
                    eco = approval.eco_id
                    stage = approval.stage_id
                    
                    if not user or not eco or not stage:
                        continue
                        
                    # Send notification
                    notification_service.notify_user(
                        user_id=user.id,
                        title="Action Required: ECO Approval Pending",
                        message=f"You have a pending approval for ECO '{eco.name}' at stage '{stage.name}'.",
                        notification_type="warning",
                        action={
                            "type": "navigate",
                            "target": f"/models/plm.eco/{eco.id}",
                            "params": {"tab": "approvals"}
                        },
                        expires_in_hours=48 # Reminders expire in 2 days
                    )
                    sent_count += 1
                except Exception as inner_e:
                    logger.error(f"Failed to send reminder for approval {approval.id}: {inner_e}")

            db.commit()
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Approval reminder process completed: sent {sent_count} reminders in {execution_time:.2f}s")
            
            return {
                "success": True, 
                "sent_count": sent_count,
                "execution_time": execution_time
            }
            
        except Exception as e:
            if not self._provided_db:
                db.rollback()
            logger.error(f"Critical error in approval reminder service: {e}")
            return {
                "success": False, 
                "error": str(e),
                "sent_count": 0
            }
        finally:
            if not self._provided_db:
                db.close()


# Global/Helper instance seekers
def get_approval_reminder_service(db: Optional[Session] = None) -> ApprovalReminderService:
    """Get the approval reminder service instance."""
    return ApprovalReminderService(db)
