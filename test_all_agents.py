import os
import subprocess
import glob
from concurrent.futures import ThreadPoolExecutor

def test_agent(agent_path):
    """Executes a single industry agent script and returns its status."""
    industry_name = agent_path.split('/')[1]
    print(f"Testing Agent: {industry_name}...")
    
    try:
        # Run the agent script. We use 'input' to simulate a simple interaction if needed, 
        # but our scripts have pre-defined queries in their __main__ block.
        result = subprocess.run(
            ['python3', agent_path],
            capture_output=True,
            text=True,
            timeout=30,
            env=os.environ
        )
        
        if result.returncode == 0:
            return f"✅ {industry_name.upper():<15} | SUCCESS"
        else:
            # Check if it failed due to missing API key
            if "API_KEY" in result.stderr or "APIKey" in result.stderr:
                return f"⚠️  {industry_name.upper():<15} | FAILED (Missing API Key)"
            return f"❌ {industry_name.upper():<15} | FAILED: {result.stderr.splitlines()[-1] if result.stderr else 'Unknown Error'}"
            
    except subprocess.TimeoutExpired:
        return f"⏰ {industry_name.upper():<15} | TIMEOUT"
    except Exception as e:
        return f"❌ {industry_name.upper():<15} | ERROR: {str(e)}"

def run_suite():
    print("="*50)
    print("🚀 INDUSTRY AI AGENT - LOCAL TEST SUITE")
    print("="*50)
    
    if not os.getenv("GEMINI_API_KEY"):
        print("\n[!] WARNING: GEMINI_API_KEY environment variable is not set.")
        print("[!] Most tests will fail or return 'Missing API Key' status.\n")

    # Find all agent.py files in industries/
    agent_files = glob.glob('industries/*/agent.py')
    
    if not agent_files:
        print("No industry agents found.")
        return

    # Run tests in parallel for speed
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(test_agent, sorted(agent_files)))

    print("\n" + "="*50)
    print("📋 FINAL TEST REPORT")
    print("="*50)
    for res in results:
        print(res)
    print("="*50)

if __name__ == "__main__":
    run_suite()
