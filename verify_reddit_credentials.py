#!/usr/bin/env python3
"""
Reddit Credentials Verification Script
"""

import praw
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_reddit_credentials():
    """Verify Reddit API credentials"""
    
    print("🔧 Reddit Credentials Verification")
    print("="*50)
    
    # Get credentials
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "CrewAI_Reddit_Tool/1.0")
    
    print(f"Client ID: {client_id[:10]}..." if client_id else "❌ Not found")
    print(f"Client Secret: {client_secret[:10]}..." if client_secret else "❌ Not found")
    print(f"User Agent: {user_agent}")
    print()
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in .env file!")
        print("\nPlease add to your .env file:")
        print("REDDIT_CLIENT_ID=your_client_id")
        print("REDDIT_CLIENT_SECRET=your_client_secret")
        print("REDDIT_USER_AGENT=CrewAI_Reddit_Tool/1.0")
        return False
    
    try:
        # Test 1: Basic connection
        print("🔍 Test 1: Basic connection...")
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            check_for_async=False
        )
        print("✅ PRAW client created successfully")
        
        # Test 2: Access public subreddit
        print("🔍 Test 2: Accessing public subreddit...")
        subreddit = reddit.subreddit("test")
        print(f"✅ Subreddit accessed: r/{subreddit.display_name}")
        
        # Test 3: Get hot posts
        print("🔍 Test 3: Getting hot posts...")
        hot_posts = list(subreddit.hot(limit=1))
        if hot_posts:
            print(f"✅ Hot posts retrieved: {hot_posts[0].title[:50]}...")
        else:
            print("⚠️  No hot posts found (this is normal for r/test)")
        
        # Test 4: Search functionality
        print("🔍 Test 4: Testing search...")
        search_results = list(subreddit.search("test", limit=1))
        if search_results:
            print(f"✅ Search working: {search_results[0].title[:50]}...")
        else:
            print("⚠️  No search results found")
        
        print("\n🎉 All tests passed! Your Reddit credentials are working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
        # Provide specific help based on error
        if "401" in str(e):
            print("\n🔧 401 Error - Authentication Failed:")
            print("This usually means:")
            print("1. Client ID is incorrect")
            print("2. Client Secret is incorrect")
            print("3. App type is not set to 'script'")
            print("\nTo fix:")
            print("1. Go to https://www.reddit.com/prefs/apps")
            print("2. Check your app settings")
            print("3. Make sure app type is 'script'")
            print("4. Copy the correct Client ID and Secret")
        
        elif "403" in str(e):
            print("\n🔧 403 Error - Forbidden:")
            print("This usually means:")
            print("1. User Agent is not descriptive enough")
            print("2. Rate limiting")
            print("\nTo fix:")
            print("1. Use a more descriptive User Agent")
            print("2. Wait a few minutes and try again")
        
        elif "404" in str(e):
            print("\n🔧 404 Error - Not Found:")
            print("This usually means:")
            print("1. Subreddit doesn't exist")
            print("2. API endpoint changed")
        
        return False

def get_new_credentials():
    """Guide user through getting new credentials"""
    print("\n🔧 How to Get New Reddit API Credentials:")
    print("="*50)
    print("1. Go to https://www.reddit.com/prefs/apps")
    print("2. Click 'Create App' or 'Create Another App'")
    print("3. Fill in the details:")
    print("   - Name: CrewAI Reddit Tool")
    print("   - App type: Select 'script'")
    print("   - Description: Reddit API tool for CrewAI")
    print("   - About URL: (leave blank)")
    print("   - Redirect URI: http://localhost:8080")
    print("4. Click 'Create app'")
    print("5. Copy the Client ID (under your app name)")
    print("6. Copy the Client Secret (labeled 'secret')")
    print("7. Add to your .env file:")
    print("   REDDIT_CLIENT_ID=your_client_id")
    print("   REDDIT_CLIENT_SECRET=your_client_secret")
    print("   REDDIT_USER_AGENT=CrewAI_Reddit_Tool/1.0")

def main():
    """Main verification function"""
    print("🚀 Reddit Credentials Verification Tool")
    print("="*50)
    
    success = verify_reddit_credentials()
    
    if not success:
        print("\n" + "="*50)
        get_new_credentials()
        print("="*50)
        print("\nAfter updating your .env file, run this script again to verify.")

if __name__ == "__main__":
    main()
