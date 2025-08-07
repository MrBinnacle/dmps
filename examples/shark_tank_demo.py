#!/usr/bin/env python3
"""
DMPS Shark Tank Filter Demo

This script demonstrates how to evaluate ideas using the brutal Shark Tank system.
"""

def shark_tank_demo():
    """Demonstrate the Shark Tank evaluation process"""
    
    print("🦈 DMPS SHARK TANK FILTER DEMO")
    print("=" * 50)
    
    # Sample ideas to evaluate
    sample_ideas = [
        {
            "name": "AI-Powered Prompt Evolution",
            "problem": "Current prompts don't improve over time",
            "solution": "Use genetic algorithms to evolve prompts automatically",
            "market": "Developers running prompts repeatedly",
            "advantage": "Complex AI that competitors can't easily replicate",
            "proof": "Theoretical - sounds cool"
        },
        {
            "name": "VS Code Extension",
            "problem": "Developers optimize prompts outside their workflow",
            "solution": "Right-click optimize prompts directly in VS Code",
            "market": "23M VS Code users, $10/month for premium features",
            "advantage": "First-mover in IDE integration space",
            "proof": "5 developers asked for this in GitHub issues"
        },
        {
            "name": "Prompt Templates Library",
            "problem": "Users start from scratch every time",
            "solution": "Pre-built templates for common use cases",
            "market": "All DMPS users, increases retention",
            "advantage": "Community-driven content moat",
            "proof": "Users frequently ask for examples in Discord"
        }
    ]
    
    print("\n🎯 EVALUATING SAMPLE IDEAS")
    print("-" * 30)
    
    for i, idea in enumerate(sample_ideas, 1):
        print(f"\n💡 IDEA {i}: {idea['name']}")
        print("=" * 40)
        
        # The 60-second pitch
        print("📝 60-SECOND PITCH:")
        print(f"PROBLEM: {idea['problem']}")
        print(f"SOLUTION: {idea['solution']}")
        print(f"MARKET: {idea['market']}")
        print(f"ADVANTAGE: {idea['advantage']}")
        print(f"PROOF: {idea['proof']}")
        
        # Shark evaluation
        print("\n🦈 SHARK ATTACK:")
        
        # Market Realist
        market_score = evaluate_market_realist(idea)
        print(f"Market Realist: {market_score}/5 ⭐")
        
        # Technical Skeptic
        tech_score = evaluate_technical_skeptic(idea)
        print(f"Technical Skeptic: {tech_score}/5 ⭐")
        
        # Competitive Analyst
        comp_score = evaluate_competitive_analyst(idea)
        print(f"Competitive Analyst: {comp_score}/5 ⭐")
        
        # UX Executioner
        ux_score = evaluate_ux_executioner(idea)
        print(f"UX Executioner: {ux_score}/5 ⭐")
        
        # Business Model Destroyer
        biz_score = evaluate_business_model(idea)
        print(f"Business Model Destroyer: {biz_score}/5 ⭐")
        
        # Final verdict
        total_score = market_score + tech_score + comp_score + ux_score + biz_score
        verdict = get_verdict(total_score)
        
        print(f"\n📊 TOTAL SCORE: {total_score}/25")
        print(f"🏆 VERDICT: {verdict}")
        
        if total_score >= 15:
            print("✅ SURVIVES THE SHARK TANK!")
        else:
            print("💀 KILLED BY THE SHARKS!")


def evaluate_market_realist(idea):
    """Evaluate from Market Realist perspective"""
    # Simulate brutal market evaluation
    if "theoretical" in idea["proof"].lower():
        return 1  # No real proof
    elif "asked for this" in idea["proof"].lower():
        return 4  # Real user demand
    elif "users" in idea["market"].lower() and "$" in idea["market"]:
        return 3  # Decent market size
    else:
        return 2  # Weak market case


def evaluate_technical_skeptic(idea):
    """Evaluate from Technical Skeptic perspective"""
    if "genetic algorithms" in idea["solution"].lower():
        return 1  # Too complex/research-y
    elif "extension" in idea["name"].lower():
        return 4  # Well-understood technology
    elif "templates" in idea["name"].lower():
        return 5  # Simple to implement
    else:
        return 3  # Moderate complexity


def evaluate_competitive_analyst(idea):
    """Evaluate from Competitive Analyst perspective"""
    if "first-mover" in idea["advantage"].lower():
        return 2  # Weak advantage
    elif "community-driven" in idea["advantage"].lower():
        return 4  # Network effects
    elif "complex AI" in idea["advantage"].lower():
        return 2  # Can be replicated
    else:
        return 3  # Moderate advantage


def evaluate_ux_executioner(idea):
    """Evaluate from UX Executioner perspective"""
    if "right-click" in idea["solution"].lower():
        return 5  # Simple UX
    elif "automatically" in idea["solution"].lower():
        return 2  # No user control
    elif "templates" in idea["solution"].lower():
        return 4  # Easy to use
    else:
        return 3  # Moderate UX


def evaluate_business_model(idea):
    """Evaluate from Business Model perspective"""
    if "$" in idea["market"]:
        return 4  # Clear revenue model
    elif "retention" in idea["market"].lower():
        return 4  # Reduces churn
    elif "developers" in idea["market"].lower():
        return 3  # Valuable user base
    else:
        return 2  # Unclear business impact


def get_verdict(score):
    """Get final verdict based on score"""
    if score >= 20:
        return "IMMEDIATE FUNDING 🚀"
    elif score >= 15:
        return "CONDITIONAL FUNDING ⚠️"
    elif score >= 10:
        return "MAJOR REVISION NEEDED 🔄"
    elif score >= 5:
        return "WEAK IDEA 👎"
    else:
        return "KILLED 💀"


def show_evaluation_criteria():
    """Show the evaluation criteria"""
    print("\n🦈 SHARK EVALUATION CRITERIA")
    print("=" * 40)
    
    criteria = {
        "Market Realist": [
            "Real user demand with evidence",
            "Clear market size and willingness to pay",
            "Competitive pricing research",
            "Revenue model with assumptions"
        ],
        "Technical Skeptic": [
            "Buildable with current technology",
            "Scalable architecture",
            "Reasonable maintenance costs",
            "Clear technical approach"
        ],
        "Competitive Analyst": [
            "Defensible competitive advantage",
            "Hard for big tech to replicate",
            "Network effects or data moats",
            "Unique positioning"
        ],
        "UX Executioner": [
            "Solves daily pain points",
            "Simple user experience",
            "Low learning curve",
            "Fits existing workflows"
        ],
        "Business Model Destroyer": [
            "Clear path to revenue",
            "Positive ROI calculation",
            "Increases retention or reduces churn",
            "Strategic business value"
        ]
    }
    
    for shark, requirements in criteria.items():
        print(f"\n🦈 {shark}:")
        for req in requirements:
            print(f"  • {req}")


def show_automatic_killers():
    """Show automatic rejection criteria"""
    print("\n💀 AUTOMATIC REJECTION CRITERIA")
    print("=" * 40)
    
    killers = [
        "Solution looking for a problem",
        "Feature creep monster",
        "Competitor copycat",
        "Perfectionist trap",
        "Resource black hole",
        "No clear user pain point",
        "Requires breakthrough research",
        "No defensible advantage",
        "No revenue model",
        "Too complex for MVP"
    ]
    
    for killer in killers:
        print(f"💀 {killer}")


def main():
    """Run the Shark Tank demo"""
    print("Welcome to the DMPS Shark Tank Filter Demo!")
    print("This system brutally evaluates ideas to ensure only brilliant ones survive.\n")
    
    while True:
        print("\nChoose an option:")
        print("1. Run idea evaluation demo")
        print("2. Show evaluation criteria")
        print("3. Show automatic rejection criteria")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            shark_tank_demo()
        elif choice == "2":
            show_evaluation_criteria()
        elif choice == "3":
            show_automatic_killers()
        elif choice == "4":
            print("\n🦈 Remember: If it's not obviously brilliant, it's obviously wrong!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()