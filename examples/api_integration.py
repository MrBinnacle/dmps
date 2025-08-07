#!/usr/bin/env python3
"""
API Integration Examples

This script demonstrates how to integrate DMPS into web APIs, 
microservices, and other applications.
"""

import json
import asyncio
from typing import Dict, List, Optional
from dmps import PromptOptimizer


class DMPSService:
    """Example service class for integrating DMPS into applications"""
    
    def __init__(self):
        self.optimizer = PromptOptimizer()
        self.cache = {}  # Simple in-memory cache
    
    def optimize_prompt(self, prompt: str, options: Dict = None) -> Dict:
        """
        Main service method for prompt optimization
        
        Args:
            prompt: The prompt to optimize
            options: Optional configuration (mode, platform, etc.)
        
        Returns:
            Dictionary with optimization results
        """
        # Extract options
        options = options or {}
        mode = options.get("mode", "conversational")
        platform = options.get("platform", "claude")
        use_cache = options.get("cache", True)
        
        # Check cache
        cache_key = f"{prompt}:{mode}:{platform}"
        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Optimize
            result, validation = self.optimizer.optimize(prompt, mode=mode, platform=platform)
            
            # Prepare response
            response = {
                "success": validation.is_valid,
                "prompt": {
                    "original": prompt,
                    "optimized": result.optimized_prompt if validation.is_valid else None
                },
                "analysis": {
                    "intent": result.metadata.get("intent") if validation.is_valid else None,
                    "improvements_count": len(result.improvements) if validation.is_valid else 0,
                    "format_type": result.format_type if validation.is_valid else None
                },
                "validation": {
                    "errors": validation.errors,
                    "warnings": validation.warnings
                },
                "metadata": result.metadata if validation.is_valid else {}
            }
            
            # Cache successful results
            if use_cache and validation.is_valid:
                self.cache[cache_key] = response
            
            return response
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "prompt": {"original": prompt, "optimized": None},
                "analysis": None,
                "validation": {"errors": [str(e)], "warnings": []},
                "metadata": {}
            }
    
    def batch_optimize(self, prompts: List[str], options: Dict = None) -> List[Dict]:
        """Batch optimization for multiple prompts"""
        return [self.optimize_prompt(prompt, options) for prompt in prompts]
    
    async def async_optimize(self, prompt: str, options: Dict = None) -> Dict:
        """Async version for non-blocking optimization"""
        # In a real implementation, you might use asyncio.to_thread()
        # or a proper async optimization pipeline
        return await asyncio.to_thread(self.optimize_prompt, prompt, options)


def example_1_rest_api_simulation():
    """Example 1: Simulating REST API endpoints"""
    print("=" * 60)
    print("EXAMPLE 1: REST API Simulation")
    print("=" * 60)
    
    service = DMPSService()
    
    # Simulate POST /optimize endpoint
    def post_optimize(request_data):
        prompt = request_data.get("prompt")
        options = request_data.get("options", {})
        
        if not prompt:
            return {"error": "Missing 'prompt' field", "status": 400}
        
        result = service.optimize_prompt(prompt, options)
        return {"data": result, "status": 200 if result["success"] else 400}
    
    # Test API calls
    test_requests = [
        {
            "prompt": "Write a technical blog post",
            "options": {"mode": "conversational", "platform": "claude"}
        },
        {
            "prompt": "Create unit tests",
            "options": {"mode": "structured", "platform": "chatgpt"}
        },
        {
            "prompt": "",  # Invalid request
            "options": {}
        }
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\nAPI Call {i}:")
        print(f"Request: {json.dumps(request, indent=2)}")
        
        response = post_optimize(request)
        print(f"Status: {response['status']}")
        
        if response["status"] == 200:
            data = response["data"]
            print(f"Success: {data['success']}")
            if data["success"]:
                print(f"Intent: {data['analysis']['intent']}")
                print(f"Improvements: {data['analysis']['improvements_count']}")
        else:
            print(f"Error: {response.get('error', 'Unknown error')}")


def example_2_microservice_pattern():
    """Example 2: Microservice integration pattern"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Microservice Pattern")
    print("=" * 60)
    
    class PromptOptimizationMicroservice:
        """Example microservice for prompt optimization"""
        
        def __init__(self):
            self.service = DMPSService()
            self.health_status = "healthy"
        
        def health_check(self):
            """Health check endpoint"""
            return {
                "status": self.health_status,
                "service": "dmps-optimizer",
                "version": "0.1.0"
            }
        
        def optimize(self, prompt, mode="conversational", platform="claude"):
            """Main optimization endpoint"""
            try:
                result = self.service.optimize_prompt(
                    prompt, 
                    {"mode": mode, "platform": platform}
                )
                return result
            except Exception as e:
                self.health_status = "degraded"
                raise e
        
        def batch_optimize(self, requests):
            """Batch optimization endpoint"""
            results = []
            for req in requests:
                result = self.optimize(
                    req["prompt"],
                    req.get("mode", "conversational"),
                    req.get("platform", "claude")
                )
                results.append(result)
            return results
    
    # Test microservice
    microservice = PromptOptimizationMicroservice()
    
    # Health check
    health = microservice.health_check()
    print(f"Health Check: {health}")
    
    # Single optimization
    result = microservice.optimize("Explain AI ethics", "structured", "claude")
    print(f"\nSingle Optimization Success: {result['success']}")
    
    # Batch optimization
    batch_requests = [
        {"prompt": "Write documentation", "mode": "conversational"},
        {"prompt": "Create test cases", "mode": "structured"}
    ]
    batch_results = microservice.batch_optimize(batch_requests)
    print(f"Batch Results: {len(batch_results)} processed")


async def example_3_async_integration():
    """Example 3: Async/await integration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Async Integration")
    print("=" * 60)
    
    service = DMPSService()
    
    # Simulate concurrent optimization requests
    prompts = [
        "Write a user manual",
        "Create API documentation", 
        "Generate test scenarios",
        "Explain system architecture"
    ]
    
    print(f"Processing {len(prompts)} prompts concurrently...")
    
    # Process all prompts concurrently
    tasks = [
        service.async_optimize(prompt, {"mode": "conversational"})
        for prompt in prompts
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Analyze results
    successful = sum(1 for r in results if r["success"])
    total_improvements = sum(r["analysis"]["improvements_count"] for r in results if r["success"])
    
    print(f"Results: {successful}/{len(prompts)} successful")
    print(f"Total improvements applied: {total_improvements}")


def example_4_webhook_integration():
    """Example 4: Webhook/callback integration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Webhook Integration")
    print("=" * 60)
    
    class WebhookOptimizer:
        """Example webhook-based optimizer"""
        
        def __init__(self):
            self.service = DMPSService()
            self.webhooks = {}  # webhook_id -> callback_url mapping
        
        def register_webhook(self, webhook_id: str, callback_url: str):
            """Register a webhook for async notifications"""
            self.webhooks[webhook_id] = callback_url
            return {"webhook_id": webhook_id, "status": "registered"}
        
        def optimize_with_webhook(self, prompt: str, webhook_id: str, options: Dict = None):
            """Optimize and send result to webhook"""
            # Simulate async processing
            result = self.service.optimize_prompt(prompt, options)
            
            # Simulate webhook call
            callback_url = self.webhooks.get(webhook_id)
            if callback_url:
                webhook_payload = {
                    "webhook_id": webhook_id,
                    "result": result,
                    "timestamp": "2024-01-01T12:00:00Z"
                }
                # In real implementation: requests.post(callback_url, json=webhook_payload)
                print(f"Webhook called: {callback_url}")
                print(f"Payload preview: {json.dumps(webhook_payload, indent=2)[:200]}...")
                return {"status": "processing", "webhook_id": webhook_id}
            else:
                return {"error": "Webhook not found", "webhook_id": webhook_id}
    
    # Test webhook integration
    webhook_optimizer = WebhookOptimizer()
    
    # Register webhook
    registration = webhook_optimizer.register_webhook("test-123", "https://api.example.com/webhook")
    print(f"Webhook Registration: {registration}")
    
    # Process with webhook
    webhook_result = webhook_optimizer.optimize_with_webhook(
        "Create a deployment guide",
        "test-123",
        {"mode": "structured"}
    )
    print(f"Webhook Processing: {webhook_result}")


def example_5_monitoring_integration():
    """Example 5: Monitoring and metrics integration"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Monitoring Integration")
    print("=" * 60)
    
    class MonitoredDMPSService(DMPSService):
        """DMPS service with monitoring capabilities"""
        
        def __init__(self):
            super().__init__()
            self.metrics = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_improvements": 0,
                "intents_detected": {},
                "platforms_used": {}
            }
        
        def optimize_prompt(self, prompt: str, options: Dict = None) -> Dict:
            """Override to add monitoring"""
            self.metrics["total_requests"] += 1
            
            result = super().optimize_prompt(prompt, options)
            
            if result["success"]:
                self.metrics["successful_requests"] += 1
                self.metrics["total_improvements"] += result["analysis"]["improvements_count"]
                
                # Track intent distribution
                intent = result["analysis"]["intent"]
                self.metrics["intents_detected"][intent] = self.metrics["intents_detected"].get(intent, 0) + 1
                
                # Track platform usage
                platform = options.get("platform", "claude") if options else "claude"
                self.metrics["platforms_used"][platform] = self.metrics["platforms_used"].get(platform, 0) + 1
            else:
                self.metrics["failed_requests"] += 1
            
            return result
        
        def get_metrics(self):
            """Get current metrics"""
            success_rate = (self.metrics["successful_requests"] / self.metrics["total_requests"]) * 100 if self.metrics["total_requests"] > 0 else 0
            
            return {
                **self.metrics,
                "success_rate": round(success_rate, 2),
                "avg_improvements": round(self.metrics["total_improvements"] / max(self.metrics["successful_requests"], 1), 2)
            }
    
    # Test monitored service
    monitored_service = MonitoredDMPSService()
    
    # Process some requests
    test_prompts = [
        ("Write code", {"platform": "claude"}),
        ("Create story", {"platform": "chatgpt"}),
        ("", {}),  # This will fail
        ("Explain concept", {"platform": "claude"})
    ]
    
    for prompt, options in test_prompts:
        monitored_service.optimize_prompt(prompt, options)
    
    # Get metrics
    metrics = monitored_service.get_metrics()
    print("Service Metrics:")
    print(json.dumps(metrics, indent=2))


def main():
    """Run all API integration examples"""
    print("DMPS API Integration Examples")
    print("This script demonstrates how to integrate DMPS into various application architectures\n")
    
    try:
        example_1_rest_api_simulation()
        example_2_microservice_pattern()
        
        # Run async example
        asyncio.run(example_3_async_integration())
        
        example_4_webhook_integration()
        example_5_monitoring_integration()
        
        print("\n" + "=" * 60)
        print("All API integration examples completed!")
        print("These patterns can be adapted for your specific architecture needs.")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running API integration examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()