#!/usr/bin/env python3
"""
Automated Training System for Email Categorization
Uses API calls to generate emails, classify them, and apply feedback for model training
"""

import requests
import json
import time
import random
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
import statistics
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)

class AutomatedTrainingSystem:
    def __init__(self, backend_url: str = "http://localhost:5000"):
        self.backend_url = backend_url
        self.training_stats = {
            "total_emails_generated": 0,
            "total_classifications": 0,
            "total_feedback_applied": 0,
            "accuracy_history": [],
            "training_sessions": []
        }
        
    def test_backend_connection(self) -> bool:
        """Test if backend server is accessible"""
        try:
            response = requests.get(f"{self.backend_url}/categories", timeout=5)
            if response.status_code == 200:
                logging.info("✅ Backend server is accessible")
                return True
            else:
                logging.error(f"❌ Backend server error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Backend connection failed: {e}")
            return False
    
    def generate_training_emails(self, count: int) -> Tuple[List[Dict], List[Dict]]:
        """
        API Call 1: Generate training emails using external LLM
        
        Args:
            count: Number of emails to generate
            
        Returns:
            Tuple of (emails, answer_key)
        """
        logging.info(f"🔄 API Call 1: Generating {count} training emails via API...")
        
        try:
            response = requests.post(
                f"{self.backend_url}/generate-emails",
                json={"count": count},
                timeout=120  # Longer timeout for LLM generation
            )
            
            if response.status_code == 200:
                data = response.json()
                emails = data["emails"]
                answer_key = data["answer_key"]
                
                self.training_stats["total_emails_generated"] += len(emails)
                logging.info(f"✅ Generated {len(emails)} emails successfully")
                
                return emails, answer_key
            else:
                error_msg = response.json().get("error", "Unknown error")
                logging.error(f"❌ Email generation failed: {error_msg}")
                return [], []
                
        except requests.exceptions.RequestException as e:
            logging.error(f"❌ Email generation API call failed: {e}")
            return [], []
    
    def classify_emails(self, emails: List[Dict]) -> List[Dict]:
        """
        API Call 2: Classify generated emails using the classification model
        
        Args:
            emails: List of emails to classify
            
        Returns:
            List of classification results
        """
        logging.info(f"🔄 API Call 2: Classifying {len(emails)} emails...")
        
        classifications = []
        
        for i, email in enumerate(emails, 1):
            try:
                response = requests.post(
                    f"{self.backend_url}/classify",
                    json={
                        "subject": email["subject"],
                        "body": email["body"]
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    classification = {
                        "email_id": email["id"],
                        "predicted_category": result["category"],
                        "confidence": result["confidence"],
                        "subject": email["subject"],
                        "body": email["body"]
                    }
                    classifications.append(classification)
                    
                    self.training_stats["total_classifications"] += 1
                    
                    if i % 5 == 0:  # Progress update every 5 emails
                        logging.info(f"  Classified {i}/{len(emails)} emails...")
                        
                else:
                    logging.warning(f"Classification failed for email {email['id']}")
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"Classification API call failed for email {email['id']}: {e}")
                continue
        
        logging.info(f"✅ Classified {len(classifications)} emails successfully")
        return classifications
    
    def apply_feedback_training(self, classifications: List[Dict], answer_key: List[Dict]) -> Dict:
        """
        API Call 3: Apply feedback for incorrect classifications to train the model
        
        Args:
            classifications: List of classification results
            answer_key: List of correct answers
            
        Returns:
            Training results summary
        """
        logging.info(f"🔄 API Call 3: Applying feedback for model training...")
        
        # Create lookup for correct answers
        correct_answers = {item["id"]: item["correct_category"] for item in answer_key}
        
        feedback_applied = 0
        correct_predictions = 0
        total_predictions = len(classifications)
        
        for classification in classifications:
            email_id = classification["email_id"]
            predicted_category = classification["predicted_category"]
            correct_category = correct_answers.get(email_id)
            
            if predicted_category == correct_category:
                correct_predictions += 1
            else:
                # Apply feedback for incorrect classification
                try:
                    feedback_response = requests.post(
                        f"{self.backend_url}/feedback",
                        json={
                            "email": {
                                "subject": classification["subject"],
                                "body": classification["body"]
                            },
                            "correct_category": correct_category
                        },
                        timeout=10
                    )
                    
                    if feedback_response.status_code == 200:
                        feedback_applied += 1
                        self.training_stats["total_feedback_applied"] += 1
                        logging.debug(f"Applied feedback for email {email_id}: {predicted_category} -> {correct_category}")
                    else:
                        logging.warning(f"Feedback API call failed for email {email_id}")
                        
                except requests.exceptions.RequestException as e:
                    logging.error(f"Feedback API call failed for email {email_id}: {e}")
                    continue
        
        accuracy = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
        self.training_stats["accuracy_history"].append(accuracy)
        
        results = {
            "total_emails": total_predictions,
            "correct_predictions": correct_predictions,
            "incorrect_predictions": total_predictions - correct_predictions,
            "feedback_applied": feedback_applied,
            "accuracy": accuracy
        }
        
        logging.info(f"✅ Training feedback applied: {feedback_applied} corrections")
        logging.info(f"📊 Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_predictions})")
        
        return results
    
    def run_training_cycle(self, email_count: int = 10) -> Dict:
        """
        Run a complete training cycle with API calls
        
        Args:
            email_count: Number of emails to generate and train on
            
        Returns:
            Training cycle results
        """
        cycle_start = datetime.now()
        logging.info(f"🚀 Starting training cycle with {email_count} emails")
        
        # Step 1: Generate emails
        emails, answer_key = self.generate_training_emails(email_count)
        if not emails:
            logging.error("❌ Training cycle failed: No emails generated")
            return {"status": "failed", "reason": "email_generation_failed"}
        
        # Step 2: Classify emails
        classifications = self.classify_emails(emails)
        if not classifications:
            logging.error("❌ Training cycle failed: No classifications completed")
            return {"status": "failed", "reason": "classification_failed"}
        
        # Step 3: Apply feedback
        training_results = self.apply_feedback_training(classifications, answer_key)
        
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        
        # Record training session
        session_data = {
            "timestamp": cycle_start.isoformat(),
            "duration_seconds": cycle_duration,
            "email_count": len(emails),
            "classifications_count": len(classifications),
            "accuracy": training_results["accuracy"],
            "feedback_applied": training_results["feedback_applied"]
        }
        
        self.training_stats["training_sessions"].append(session_data)
        
        logging.info(f"✅ Training cycle completed in {cycle_duration:.1f} seconds")
        
        return {
            "status": "success",
            "session_data": session_data,
            "training_results": training_results
        }
    
    def run_continuous_training(self, cycles: int = 5, emails_per_cycle: int = 10, 
                              delay_between_cycles: int = 30) -> Dict:
        """
        Run multiple training cycles continuously
        
        Args:
            cycles: Number of training cycles to run
            emails_per_cycle: Number of emails per cycle
            delay_between_cycles: Delay in seconds between cycles
            
        Returns:
            Overall training results
        """
        logging.info(f"🔄 Starting continuous training: {cycles} cycles, {emails_per_cycle} emails each")
        
        overall_start = datetime.now()
        successful_cycles = 0
        failed_cycles = 0
        
        for cycle_num in range(1, cycles + 1):
            logging.info(f"\n{'='*50}")
            logging.info(f"TRAINING CYCLE {cycle_num}/{cycles}")
            logging.info(f"{'='*50}")
            
            result = self.run_training_cycle(emails_per_cycle)
            
            if result["status"] == "success":
                successful_cycles += 1
                logging.info(f"✅ Cycle {cycle_num} completed successfully")
            else:
                failed_cycles += 1
                logging.error(f"❌ Cycle {cycle_num} failed: {result.get('reason', 'unknown')}")
            
            # Delay between cycles (except for the last one)
            if cycle_num < cycles:
                logging.info(f"⏳ Waiting {delay_between_cycles} seconds before next cycle...")
                time.sleep(delay_between_cycles)
        
        overall_end = datetime.now()
        total_duration = (overall_end - overall_start).total_seconds()
        
        # Calculate overall statistics
        overall_results = {
            "total_cycles": cycles,
            "successful_cycles": successful_cycles,
            "failed_cycles": failed_cycles,
            "total_duration_seconds": total_duration,
            "total_emails_generated": self.training_stats["total_emails_generated"],
            "total_classifications": self.training_stats["total_classifications"],
            "total_feedback_applied": self.training_stats["total_feedback_applied"],
            "average_accuracy": statistics.mean(self.training_stats["accuracy_history"]) if self.training_stats["accuracy_history"] else 0,
            "accuracy_trend": self.training_stats["accuracy_history"]
        }
        
        logging.info(f"\n{'='*50}")
        logging.info(f"CONTINUOUS TRAINING COMPLETED")
        logging.info(f"{'='*50}")
        logging.info(f"✅ Successful cycles: {successful_cycles}/{cycles}")
        logging.info(f"📧 Total emails processed: {overall_results['total_emails_generated']}")
        logging.info(f"🎯 Total classifications: {overall_results['total_classifications']}")
        logging.info(f"📚 Total feedback applied: {overall_results['total_feedback_applied']}")
        logging.info(f"📊 Average accuracy: {overall_results['average_accuracy']:.1f}%")
        logging.info(f"⏱️  Total duration: {total_duration:.1f} seconds")
        
        return overall_results
    
    def save_training_stats(self, filename: str = None):
        """Save training statistics to file"""
        if filename is None:
            filename = f"training_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.training_stats, f, indent=2)
        
        logging.info(f"📁 Training statistics saved to {filename}")
    
    def display_training_summary(self):
        """Display a summary of training statistics"""
        print(f"\n{'='*60}")
        print("TRAINING SYSTEM SUMMARY")
        print(f"{'='*60}")
        print(f"📧 Total emails generated: {self.training_stats['total_emails_generated']}")
        print(f"🎯 Total classifications: {self.training_stats['total_classifications']}")
        print(f"📚 Total feedback applied: {self.training_stats['total_feedback_applied']}")
        print(f"🔄 Training sessions: {len(self.training_stats['training_sessions'])}")
        
        if self.training_stats['accuracy_history']:
            print(f"📊 Average accuracy: {statistics.mean(self.training_stats['accuracy_history']):.1f}%")
            print(f"📈 Best accuracy: {max(self.training_stats['accuracy_history']):.1f}%")
            print(f"📉 Worst accuracy: {min(self.training_stats['accuracy_history']):.1f}%")
            
            if len(self.training_stats['accuracy_history']) > 1:
                trend = "improving" if self.training_stats['accuracy_history'][-1] > self.training_stats['accuracy_history'][0] else "declining"
                print(f"📊 Accuracy trend: {trend}")


def main():
    parser = argparse.ArgumentParser(description="Automated Training System for Email Categorization")
    parser.add_argument("--backend-url", type=str, default="http://localhost:5000", 
                       help="Backend server URL")
    parser.add_argument("--cycles", type=int, default=3, 
                       help="Number of training cycles to run")
    parser.add_argument("--emails-per-cycle", type=int, default=10, 
                       help="Number of emails to generate per cycle")
    parser.add_argument("--delay", type=int, default=30, 
                       help="Delay in seconds between cycles")
    parser.add_argument("--single-cycle", action="store_true", 
                       help="Run only a single training cycle")
    parser.add_argument("--save-stats", type=str, 
                       help="Save training statistics to specified file")
    
    args = parser.parse_args()
    
    # Initialize training system
    trainer = AutomatedTrainingSystem(backend_url=args.backend_url)
    
    # Test backend connection
    if not trainer.test_backend_connection():
        print("❌ Cannot connect to backend server. Please ensure:")
        print("1. Backend server is running: python backend/app.py")
        print("2. OpenAI API key is set: export OPENAI_API_KEY='your-key'")
        print("3. Backend URL is correct:", args.backend_url)
        return
    
    try:
        if args.single_cycle:
            # Run single training cycle
            print(f"🚀 Running single training cycle with {args.emails_per_cycle} emails")
            result = trainer.run_training_cycle(args.emails_per_cycle)
            
            if result["status"] == "success":
                print("✅ Training cycle completed successfully!")
                trainer.display_training_summary()
            else:
                print(f"❌ Training cycle failed: {result.get('reason', 'unknown')}")
        else:
            # Run continuous training
            print(f"🔄 Starting continuous training...")
            print(f"   Cycles: {args.cycles}")
            print(f"   Emails per cycle: {args.emails_per_cycle}")
            print(f"   Delay between cycles: {args.delay} seconds")
            
            results = trainer.run_continuous_training(
                cycles=args.cycles,
                emails_per_cycle=args.emails_per_cycle,
                delay_between_cycles=args.delay
            )
            
            trainer.display_training_summary()
        
        # Save statistics if requested
        if args.save_stats:
            trainer.save_training_stats(args.save_stats)
        
    except KeyboardInterrupt:
        print("\n⏹️  Training interrupted by user")
        trainer.display_training_summary()
    except Exception as e:
        logging.error(f"❌ Training system error: {e}")
        print(f"❌ Training system error: {e}")


if __name__ == "__main__":
    main()