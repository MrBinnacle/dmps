#!/usr/bin/env python3
"""
DMPS First Principles Thinking Demo

This script demonstrates how to apply first principles thinking to idea evaluation.
"""

def first_principles_demo():
    """Demonstrate first principles evaluation process"""
    
    print("🧠 DMPS FIRST PRINCIPLES THINKING DEMO")
    print("=" * 50)
    
    # Sample ideas to evaluate with first principles
    sample_ideas = [
        {
            "name": "AI-Powered Prompt Evolution",
            "traditional_problem": "Prompts don't improve over time",
            "fundamental_problem": "Users want better results with less effort",
            "traditional_solution": "Use genetic algorithms to evolve prompts",
            "simplest_solution": "Let users rate prompts and show top-rated ones",
            "assumptions": ["Users run same prompts repeatedly", "Marginal improvements matter", "Users want automation over control"],
            "evidence": "Theoretical - sounds advanced",
            "value_proof": "Slightly better prompts after many iterations"
        },
        {
            "name": "VS Code Extension", 
            "traditional_problem": "Developers optimize prompts outside their workflow",
            "fundamental_problem": "Context switching wastes mental energy",
            "traditional_solution": "Build VS Code extension with full DMPS features",
            "simplest_solution": "Right-click menu to optimize selected text",
            "assumptions": ["Developers use VS Code", "They optimize prompts frequently", "Integration saves meaningful time"],
            "evidence": "5 developers requested this in GitHub issues",
            "value_proof": "Increased daily usage of DMPS"
        },
        {
            "name": "Enterprise Team Dashboard",
            "traditional_problem": "Teams need to collaborate on prompts",
            "fundamental_problem": "Knowledge sharing improves team performance", 
            "traditional_solution": "Build full collaboration platform with sharing, comments, versions",
            "simplest_solution": "Export/import prompt templates",
            "assumptions": ["Teams work on prompts together", "Collaboration improves results", "Teams will pay for this"],
            "evidence": "No direct user requests, but enterprise tools usually have dashboards",
            "value_proof": "Team productivity metrics"
        }
    ]
    
    print("\n🔍 FIRST PRINCIPLES EVALUATION")
    print("-" * 40)
    
    for i, idea in enumerate(sample_ideas, 1):
        print(f"\n💡 IDEA {i}: {idea['name']}")
        print("=" * 50)
        
        # Traditional vs First Principles comparison
        print("🔄 TRADITIONAL THINKING:")
        print(f"Problem: {idea['traditional_problem']}")
        print(f"Solution: {idea['traditional_solution']}")
        print(f"Evidence: {idea['evidence']}")
        
        print("\n🧠 FIRST PRINCIPLES THINKING:")
        print(f"Fundamental Problem: {idea['fundamental_problem']}")
        print(f"Simplest Solution: {idea['simplest_solution']}")
        print(f"Key Assumptions: {', '.join(idea['assumptions'])}")
        print(f"Value Proof: {idea['value_proof']}")
        
        # Apply first principles tests
        print(f"\n🧪 FIRST PRINCIPLES TESTS:")
        
        # The 5 Whys Test
        five_whys_score = apply_five_whys_test(idea)
        print(f"5 Whys Test: {five_whys_score}/5 ⭐")
        
        # The Alien Test
        alien_score = apply_alien_test(idea)
        print(f"Alien Test: {alien_score}/5 ⭐")
        
        # The 10x Constraint Test
        constraint_score = apply_constraint_test(idea)
        print(f"10x Constraint Test: {constraint_score}/5 ⭐")
        
        # Overall first principles score
        total_score = five_whys_score + alien_score + constraint_score
        verdict = get_first_principles_verdict(total_score)
        
        print(f"\n📊 FIRST PRINCIPLES SCORE: {total_score}/15")
        print(f"🏆 VERDICT: {verdict}")
        
        if total_score >= 12:
            print("✅ PASSES FIRST PRINCIPLES TEST!")
        else:
            print("❌ FAILS FIRST PRINCIPLES TEST!")


def apply_five_whys_test(idea):
    """Apply the 5 Whys test to understand fundamental need"""
    # Simulate the 5 whys evaluation
    if "context switching" in idea["fundamental_problem"]:
        return 5  # Clear fundamental need
    elif "better results" in idea["fundamental_problem"]:
        return 3  # Somewhat fundamental
    elif "team performance" in idea["fundamental_problem"]:
        return 2  # Vague fundamental need
    else:
        return 1  # No clear fundamental need


def apply_alien_test(idea):
    """Apply the Alien Test - can someone with no context understand this?"""
    if "right-click menu" in idea["simplest_solution"]:
        return 5  # Immediately understandable
    elif "export/import" in idea["simplest_solution"]:
        return 4  # Pretty clear
    elif "show top-rated" in idea["simplest_solution"]:
        return 3  # Somewhat clear
    else:
        return 2  # Confusing


def apply_constraint_test(idea):
    """Apply the 10x Constraint Test - what would you build with 10x fewer resources?"""
    if idea["simplest_solution"] == idea["traditional_solution"]:
        return 2  # No simplification
    elif "right-click" in idea["simplest_solution"]:
        return 5  # Dramatically simplified
    elif "export/import" in idea["simplest_solution"]:
        return 4  # Well simplified
    else:
        return 3  # Somewhat simplified


def get_first_principles_verdict(score):
    """Get verdict based on first principles score"""
    if score >= 12:
        return "FIRST PRINCIPLES APPROVED 🧠"
    elif score >= 9:
        return "NEEDS FIRST PRINCIPLES REFINEMENT 🔄"
    elif score >= 6:
        return "WEAK FIRST PRINCIPLES FOUNDATION ⚠️"
    else:
        return "FIRST PRINCIPLES FAILURE ❌"


def show_first_principles_framework():
    """Show the first principles framework"""
    print("\n🧠 FIRST PRINCIPLES FRAMEWORK")
    print("=" * 40)
    
    principles = {
        "Truth Over Comfort": "Brutal honesty about reality, even when it hurts",
        "User Value Over Feature Count": "One feature that solves a real problem > 10 features nobody needs",
        "Simplicity Over Complexity": "The simplest solution that works is usually the best solution",
        "Evidence Over Opinion": "Data and user feedback trump internal preferences", 
        "Sustainability Over Speed": "Build for long-term success, not short-term wins"
    }
    
    for principle, description in principles.items():
        print(f"\n🎯 {principle}:")
        print(f"   {description}")


def show_first_principles_tests():
    """Show the first principles tests"""
    print("\n🧪 FIRST PRINCIPLES TESTS")
    print("=" * 40)
    
    tests = {
        "The 5 Whys Test": [
            "Why do we want to build this?",
            "Why is that important?", 
            "Why does that matter?",
            "Why is that valuable?",
            "Why should users care?"
        ],
        "The Alien Test": [
            "Explain to someone with no context",
            "If they don't understand the problem, it's not fundamental",
            "If they don't see why your solution is obvious, it's not simple",
            "If they ask 'why not just...', you haven't thought from first principles"
        ],
        "The 10x Constraint Test": [
            "If you had 10x less time/money/people, what would you build?",
            "What would you cut first?",
            "What's truly essential?",
            "The constrained version is usually closer to first principles"
        ]
    }
    
    for test_name, questions in tests.items():
        print(f"\n🔬 {test_name}:")
        for question in questions:
            print(f"   • {question}")


def show_red_flags():
    """Show first principles red flags"""
    print("\n🚩 FIRST PRINCIPLES RED FLAGS")
    print("=" * 40)
    
    red_flags = [
        "\"Because everyone else does it\" - What fundamental need does this serve?",
        "\"More is better\" - Does this solve a core problem better?", 
        "\"Technology for technology's sake\" - What user problem does this solve?",
        "\"Future-proofing\" - What evidence supports this future need?",
        "\"Users might want this\" - What evidence shows they actually do?",
        "\"It would be cool if...\" - What basic human need does this serve?",
        "\"Industry best practices\" - What fundamental principle makes this right?"
    ]
    
    for flag in red_flags:
        print(f"🚩 {flag}")


def main():
    """Run the First Principles demo"""
    print("Welcome to the DMPS First Principles Thinking Demo!")
    print("This system ensures ideas are built on solid foundations, not assumptions.\n")
    
    while True:
        print("\nChoose an option:")
        print("1. Run first principles evaluation demo")
        print("2. Show first principles framework")
        print("3. Show first principles tests")
        print("4. Show first principles red flags")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            first_principles_demo()
        elif choice == "2":
            show_first_principles_framework()
        elif choice == "3":
            show_first_principles_tests()
        elif choice == "4":
            show_red_flags()
        elif choice == "5":
            print("\n🧠 Remember: Question everything, assume nothing, build from fundamentals!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()