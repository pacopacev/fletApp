#!/usr/bin/env python3
# generate_test_fingerprint.py

import subprocess
import json
import tempfile
import os

def create_test_audio():
    """Create a test audio file with actual music"""
    
    # Create a temp file
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        temp_file = f.name
    
    try:
        # Download a known music sample (SoundHelix example - public domain)
        print("Downloading test music sample...")
        cmd = [
            'wget', '-q', 
            'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            '-O', temp_file
        ]
        
        result = subprocess.run(cmd, timeout=30)
        
        if result.returncode == 0 and os.path.exists(temp_file):
            print(f"✓ Downloaded test audio: {os.path.getsize(temp_file)} bytes")
            
            # Generate fingerprint
            print("Generating fingerprint...")
            cmd = ['fpcalc', '-json', '-length', '30', temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                fingerprint = data.get('fingerprint', '')
                duration = data.get('duration', 0)
                
                if fingerprint:
                    print(f"\n✅ Valid fingerprint generated!")
                    print(f"Duration: {duration}s")
                    print(f"Fingerprint length: {len(fingerprint)} chars")
                    print(f"First 100 chars: {fingerprint[:100]}")
                    
                    # Test with AcoustID demo
                    test_with_fingerprint(fingerprint, duration)
                    return fingerprint, duration
                    
        return None, None
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_with_fingerprint(fingerprint, duration):
    """Test the fingerprint with AcoustID demo API"""
    
    import requests
    
    DEMO_KEY = "1vOwZtEn"
    url = "https://api.acoustid.org/v2/lookup"
    
    params = {
        'client': DEMO_KEY,
        'duration': str(int(duration)),
        'fingerprint': fingerprint,
        'meta': 'recordings',
        'format': 'json'
    }
    
    print(f"\nTesting fingerprint with AcoustID...")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'ok':
                print("✅ AcoustID API works with real fingerprint!")
                
                if data.get('results'):
                    results = data['results']
                    print(f"Found {len(results)} potential matches:")
                    
                    for i, result in enumerate(results[:3]):
                        score = result.get('score', 0)
                        if 'recordings' in result and result['recordings']:
                            recording = result['recordings'][0]
                            title = recording.get('title', 'Unknown')
                            artists = [a.get('name', 'Unknown') for a in recording.get('artists', [])]
                            print(f"  {i+1}. Score: {score:.3f} -> {title} by {', '.join(artists)}")
                else:
                    print("⚠ No matches found (sample might not be in database)")
            else:
                print(f"❌ API Error: {data.get('error', {}).get('message')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("="*60)
    print("GENERATING VALID FINGERPRINT FOR TESTING")
    print("="*60)
    
    fingerprint, duration = create_test_audio()
    
    if fingerprint:
        print(f"\n✅ Success! Use this for testing:")
        print(f"Fingerprint (first 200 chars): {fingerprint[:200]}")
        print(f"Duration: {duration}")
    else:
        print("\n❌ Failed to generate fingerprint")
        print("\nInstall wget if missing: sudo apt install wget")