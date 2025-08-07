# Hard Right Over Easy Wrong Rule

## Rule
Always choose the correct, sustainable solution over quick fixes that create technical debt.

## Rationale
- Quick fixes compound into major problems
- Proper solutions prevent future issues
- Technical debt slows development velocity
- Quality code is maintainable code

## Examples

### ❌ Easy Wrong
- Removing API keys instead of fixing .gitignore
- Using `# type: ignore` instead of proper type handling
- Hardcoding values instead of configuration
- Copy-pasting code instead of creating abstractions
- Suppressing errors instead of handling them

### ✅ Hard Right
- Setting up proper .gitignore and environment management
- Using TYPE_CHECKING pattern for optional dependencies
- Creating configuration systems
- Building reusable components and base classes
- Implementing proper error handling and fallbacks

## Implementation
- Identify root cause, not just symptoms
- Design for maintainability and extensibility
- Follow established patterns and best practices
- Consider long-term implications
- Invest time upfront to save time later

## Decision Framework
1. **Will this solution scale?**
2. **Will this create technical debt?**
3. **Does this follow best practices?**
4. **Will future developers understand this?**
5. **Is this the right way to solve the problem?**

If any answer is "no", choose the harder but correct solution.