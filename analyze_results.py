import pandas as pd

df = pd.read_csv('evaluation_results/detailed_results.csv')

# Filter successful queries (those with actual answers, not errors)
successful = df[df['answer'].str.len() > 100]  # Real answers are longer than error messages

print("="*60)
print("EVALUATION RESULTS ANALYSIS")
print("="*60)
print(f"\nTotal queries: {len(df)}")
print(f"Successful queries: {len(successful)}")
print(f"Failed queries (rate limited): {len(df) - len(successful)}")

if len(successful) > 0:
    print(f"\n--- SUCCESSFUL QUERIES METRICS ---")
    print(f"Average Groundedness: {successful['groundedness_score'].mean():.2%}")
    print(f"Average Citation Accuracy: {successful['citation_accuracy_score'].mean():.2%}")
    print(f"Average Latency: {successful['latency_ms'].mean():.0f}ms")
    print(f"Median Latency: {successful['latency_ms'].median():.0f}ms")
    
    print(f"\n--- BY CATEGORY ---")
    for category in successful['category'].unique():
        cat_data = successful[successful['category'] == category]
        print(f"\n{category}:")
        print(f"  Queries: {len(cat_data)}")
        print(f"  Groundedness: {cat_data['groundedness_score'].mean():.2%}")
        print(f"  Citation Accuracy: {cat_data['citation_accuracy_score'].mean():.2%}")
        print(f"  Latency: {cat_data['latency_ms'].mean():.0f}ms")

print("\n" + "="*60)
