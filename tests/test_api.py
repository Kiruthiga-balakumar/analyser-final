"""
Simple test script to verify API connectivity and basic functionality.
"""
import requests
import json
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

def test_health():
    """Test API health endpoint."""
    print("Testing API health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"✓ Health check passed: {response.json()}\n")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        print("Make sure backend is running: cd backend && python main.py\n")
        return False

def test_analyze_text():
    """Test analyze endpoint with text."""
    print("Testing text analysis...")
    
    resume_text = """
    Senior Software Engineer with 5+ years experience
    Skills: Python, JavaScript, React, Django, Docker, Kubernetes, AWS, PostgreSQL
    """
    
    job_description = """
    Senior Software Developer required
    Must have: Python, JavaScript, React, Docker, AWS, PostgreSQL, Kubernetes
    Nice to have: Machine Learning, GraphQL
    """
    
    try:
        response = requests.post(
            f"{API_URL}/analyze-text",
            json={
                "resume_text": resume_text,
                "job_description": job_description
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Analysis successful!")
            print(f"  ATS Score: {result['ats_score']}/100")
            print(f"  Matched Skills: {len(result['matched_skills'])}")
            print(f"  Missing Skills: {len(result['missing_skills'])}")
            print(f"  Processing Time: {result['processing_time']}s\n")
            return True
        else:
            print(f"✗ Analysis failed: {response.json()}\n")
            return False
    except Exception as e:
        print(f"✗ Test failed: {e}\n")
        return False

def test_sample_files():
    """Test with sample data files."""
    print("Testing with sample data...")
    
    sample_dir = Path("sample_data")
    resume_file = sample_dir / "sample_resume.txt"
    job_file = sample_dir / "sample_job_description.txt"
    
    if not resume_file.exists() or not job_file.exists():
        print("✗ Sample files not found\n")
        return False
    
    try:
        with open(resume_file) as f:
            resume_text = f.read()
        with open(job_file) as f:
            job_description = f.read()
        
        response = requests.post(
            f"{API_URL}/analyze-text",
            json={
                "resume_text": resume_text,
                "job_description": job_description
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Sample analysis successful!")
            print(f"  ATS Score: {result['ats_score']}/100")
            print(f"  Matched: {len(result['matched_skills'])} skills")
            print(f"  Missing: {len(result['missing_skills'])} skills")
            print(f"  Time: {result['processing_time']}s")
            print(f"\n  Sample matched skills: {result['matched_skills'][:5]}")
            print(f"  Sample missing skills: {result['missing_skills'][:3]}\n")
            return True
        else:
            print(f"✗ Sample analysis failed: {response.json()}\n")
            return False
    except Exception as e:
        print(f"✗ Sample test failed: {e}\n")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Resume Analyzer - API Test Suite")
    print("=" * 60 + "\n")
    
    tests = [
        ("Health Check", test_health),
        ("Text Analysis", test_analyze_text),
        ("Sample Files", test_sample_files),
    ]
    
    results = []
    for name, test_func in tests:
        results.append((name, test_func()))
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! Application is ready to use.")
        print("\nNext steps:")
        print("1. Open frontend: http://localhost:8501")
        print("2. Upload a resume and paste a job description")
        print("3. Click 'Analyze' to get ATS score and recommendations")
    else:
        print("\n✗ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("- Ensure backend is running: cd backend && python main.py")
        print("- Check that port 8000 is available")
        print("- Verify all dependencies installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
