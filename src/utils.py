import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindabilityStatus:
    """Data class to represent the findability status of a SKU"""
    sku: str
    status: str
    confidence_score: float
    last_updated: datetime
    details: Dict
    recommendations: List[str]


class SKUFindabilityChecker:
    """Class to check and manage SKU findability status"""
    
    def __init__(self):
        # Mock database - in a real implementation, this would connect to your actual database
        self.mock_sku_database = {
            "AA0001": {
                "status": "FOUND",
                "confidence_score": 0.95,
                "last_updated": "2024-01-15T10:30:00",
                "details": {
                    "location": "Warehouse A, Section 3, Shelf 2",
                    "quantity": 150,
                    "condition": "Good",
                    "category": "Electronics",
                    "supplier": "TechCorp Inc."
                },
                "recommendations": [
                    "SKU is easily locatable with clear labeling",
                    "Consider adding RFID tags for better tracking",
                    "Stock levels are adequate for current demand"
                ]
            },
            "BB0002": {
                "status": "PARTIALLY_FOUND",
                "confidence_score": 0.65,
                "last_updated": "2024-01-14T15:45:00",
                "details": {
                    "location": "Warehouse B, Section 1 (approximate)",
                    "quantity": 25,
                    "condition": "Good",
                    "category": "Clothing",
                    "supplier": "FashionPlus Ltd."
                },
                "recommendations": [
                    "Improve location accuracy with better signage",
                    "Consider reorganizing warehouse layout",
                    "Implement barcode scanning system"
                ]
            },
            "CC0003": {
                "status": "NOT_FOUND",
                "confidence_score": 0.10,
                "last_updated": "2024-01-13T09:15:00",
                "details": {
                    "location": "Unknown",
                    "quantity": 0,
                    "condition": "Unknown",
                    "category": "Home & Garden",
                    "supplier": "GreenThumb Co."
                },
                "recommendations": [
                    "Conduct full warehouse audit",
                    "Check for misplacement in wrong sections",
                    "Verify if SKU was returned to supplier",
                    "Update inventory management system"
                ]
            }
        }
    
    def get_findability_status(self, sku: str) -> Optional[FindabilityStatus]:
        """
        Get the findability status for a specific SKU
        
        Args:
            sku (str): The SKU to check
            
        Returns:
            Optional[FindabilityStatus]: The findability status or None if SKU not found
        """
        if sku not in self.mock_sku_database:
            return None
        
        sku_data = self.mock_sku_database[sku]
        
        return FindabilityStatus(
            sku=sku,
            status=sku_data["status"],
            confidence_score=sku_data["confidence_score"],
            last_updated=datetime.fromisoformat(sku_data["last_updated"]),
            details=sku_data["details"],
            recommendations=sku_data["recommendations"]
        )
    
    def get_all_sku_statuses(self) -> List[FindabilityStatus]:
        """
        Get findability status for all SKUs in the database
        
        Returns:
            List[FindabilityStatus]: List of all SKU findability statuses
        """
        return [self.get_findability_status(sku) for sku in self.mock_sku_database.keys()]
    
    def update_sku_status(self, sku: str, new_status: str, confidence_score: float, 
                         details: Dict, recommendations: List[str]) -> bool:
        """
        Update the findability status for a SKU
        
        Args:
            sku (str): The SKU to update
            new_status (str): New status
            confidence_score (float): New confidence score
            details (Dict): New details
            recommendations (List[str]): New recommendations
            
        Returns:
            bool: True if update successful, False otherwise
        """
        if sku not in self.mock_sku_database:
            return False
        
        self.mock_sku_database[sku] = {
            "status": new_status,
            "confidence_score": confidence_score,
            "last_updated": datetime.now().isoformat(),
            "details": details,
            "recommendations": recommendations
        }
        
        return True
    
    def add_new_sku(self, sku: str, status: str, confidence_score: float,
                    details: Dict, recommendations: List[str]) -> bool:
        """
        Add a new SKU to the database
        
        Args:
            sku (str): The new SKU
            status (str): Initial status
            confidence_score (float): Initial confidence score
            details (Dict): Initial details
            recommendations (List[str]): Initial recommendations
            
        Returns:
            bool: True if addition successful, False if SKU already exists
        """
        if sku in self.mock_sku_database:
            return False
        
        self.mock_sku_database[sku] = {
            "status": status,
            "confidence_score": confidence_score,
            "last_updated": datetime.now().isoformat(),
            "details": details,
            "recommendations": recommendations
        }
        
        return True


def find_sku_findability_status(sku: str) -> Optional[FindabilityStatus]:
    """
    Convenience function to quickly get findability status for a SKU
    
    Args:
        sku (str): The SKU to check
        
    Returns:
        Optional[FindabilityStatus]: The findability status or None if not found
    """
    checker = SKUFindabilityChecker()
    return checker.get_findability_status(sku)


def print_findability_report(sku: str):
    """
    Print a formatted findability report for a SKU
    
    Args:
        sku (str): The SKU to report on
    """
    status = find_sku_findability_status(sku)
    
    if status is None:
        print(f"❌ SKU {sku} not found in database")
        return
    
    print(f"\n📦 SKU Findability Report for {sku}")
    print("=" * 50)
    print(f"Status: {status.status}")
    print(f"Confidence Score: {status.confidence_score:.2f}")
    print(f"Last Updated: {status.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📍 Location Details:")
    for key, value in status.details.items():
        print(f"  {key.title()}: {value}")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(status.recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("=" * 50)


if __name__ == "__main__":
    # Example usage
    print("🔍 SKU Findability Status Checker")
    print("=" * 40)
    
    # Check specific SKU
    target_sku = "AA0001"
    print_findability_report(target_sku)
    
    # Show all SKUs
    print("\n📊 All SKU Statuses:")
    checker = SKUFindabilityChecker()
    all_statuses = checker.get_all_sku_statuses()
    
    for status in all_statuses:
        print(f"  {status.sku}: {status.status} (Confidence: {status.confidence_score:.2f})")


