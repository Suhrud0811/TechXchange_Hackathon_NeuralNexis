#!/usr/bin/env python3
"""
Custom Reddit Tool for CrewAI Agents
"""

import praw
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RedditSearchTool:
    """Custom Reddit search tool for CrewAI agents"""
    
    def __init__(self):
        """Initialize Reddit client"""
        # Use the credentials from reddit_connect.py if env vars are not set
        client_id = os.getenv("REDDIT_CLIENT_ID", "xxwojwgZSet7HZU_4LQ_CQ")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET", "Tfbia7HVuSLbqF-s-5Ma5aXpY6jaw")
        user_agent = os.getenv("REDDIT_USER_AGENT", "crew-chatbot/0.1")
        
        try:
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                check_for_async=False
            )
            # Test the connection by trying to access a public subreddit
            test_subreddit = self.reddit.subreddit("test")
            test_subreddit.id  # This will fail if credentials are invalid
            self.authenticated = True
        except Exception as e:
            print(f"⚠️  Reddit authentication failed: {str(e)}")
            print("🔓 Falling back to public Reddit API (limited functionality)")
            self.authenticated = False
            # Initialize a basic client for public access
            self.reddit = praw.Reddit(
                client_id="public_client",
                client_secret="public_secret", 
                user_agent=user_agent,
                check_for_async=False
            )
    
    def search_subreddit(self, subreddit_name: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for posts in a specific subreddit
        
        Args:
            subreddit_name: Name of the subreddit to search
            query: Search query
            limit: Maximum number of posts to return
            
        Returns:
            List of post dictionaries
        """
        try:
            if not self.authenticated:
                return [{"error": "Reddit authentication required for search functionality. Please check your API credentials."}]
            
            subreddit = self.reddit.subreddit(subreddit_name)
            search_results = subreddit.search(query, limit=limit)
            
            posts = []
            for post in search_results:
                posts.append({
                    'title': post.title,
                    'author': str(post.author),
                    'score': post.score,
                    'url': post.url,
                    'created_utc': post.created_utc,
                    'num_comments': post.num_comments,
                    'selftext': post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext
                })
            
            return posts
            
        except Exception as e:
            return [{"error": f"Failed to search subreddit: {str(e)}"}]
    
    def get_hot_posts(self, subreddit_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get hot posts from a subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Maximum number of posts to return
            
        Returns:
            List of post dictionaries
        """
        try:
            if not self.authenticated:
                return [{"error": "Reddit authentication required for hot posts functionality. Please check your API credentials."}]
            
            subreddit = self.reddit.subreddit(subreddit_name)
            hot_posts = subreddit.hot(limit=limit)
            
            posts = []
            for post in hot_posts:
                posts.append({
                    'title': post.title,
                    'author': str(post.author),
                    'score': post.score,
                    'url': post.url,
                    'created_utc': post.created_utc,
                    'num_comments': post.num_comments,
                    'selftext': post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext
                })
            
            return posts
            
        except Exception as e:
            return [{"error": f"Failed to get hot posts: {str(e)}"}]
    
    def get_top_posts(self, subreddit_name: str, time_filter: str = "week", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get top posts from a subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            time_filter: Time filter (hour, day, week, month, year, all)
            limit: Maximum number of posts to return
            
        Returns:
            List of post dictionaries
        """
        try:
            if not self.authenticated:
                return [{"error": "Reddit authentication required for top posts functionality. Please check your API credentials."}]
            
            subreddit = self.reddit.subreddit(subreddit_name)
            top_posts = subreddit.top(time_filter=time_filter, limit=limit)
            
            posts = []
            for post in top_posts:
                posts.append({
                    'title': post.title,
                    'author': str(post.author),
                    'score': post.score,
                    'url': post.url,
                    'created_utc': post.created_utc,
                    'num_comments': post.num_comments,
                    'selftext': post.selftext[:500] + "..." if len(post.selftext) > 500 else post.selftext
                })
            
            return posts
            
        except Exception as e:
            return [{"error": f"Failed to get top posts: {str(e)}"}]
    
    def analyze_sentiment(self, subreddit_name: str, query: str, limit: int = 20) -> Dict[str, Any]:
        """
        Analyze sentiment and trends in a subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            query: Search query
            limit: Maximum number of posts to analyze
            
        Returns:
            Analysis results
        """
        posts = self.search_subreddit(subreddit_name, query, limit)
        
        if not posts or "error" in posts[0]:
            return {"error": "No posts found or error occurred"}
        
        # Simple analysis
        total_score = sum(post.get('score', 0) for post in posts)
        total_comments = sum(post.get('num_comments', 0) for post in posts)
        avg_score = total_score / len(posts) if posts else 0
        avg_comments = total_comments / len(posts) if posts else 0
        
        # Get top posts by score
        top_posts = sorted(posts, key=lambda x: x.get('score', 0), reverse=True)[:5]
        
        return {
            'subreddit': subreddit_name,
            'query': query,
            'total_posts_analyzed': len(posts),
            'average_score': round(avg_score, 2),
            'average_comments': round(avg_comments, 2),
            'total_score': total_score,
            'total_comments': total_comments,
            'top_posts': top_posts
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Reddit connection and return status
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if not self.authenticated:
                return {
                    "status": "failed",
                    "message": "Reddit authentication failed",
                    "authenticated": False,
                    "suggestion": "Please check your Reddit API credentials"
                }
            
            # Try to access a public subreddit
            test_subreddit = self.reddit.subreddit("test")
            test_posts = list(test_subreddit.hot(limit=1))
            
            if test_posts:
                return {
                    "status": "success",
                    "message": "Reddit connection working",
                    "authenticated": True,
                    "test_post": test_posts[0].title
                }
            else:
                return {
                    "status": "partial",
                    "message": "Connected but no posts found",
                    "authenticated": True
                }
                
        except Exception as e:
            return {
                "status": "failed",
                "message": f"Connection test failed: {str(e)}",
                "authenticated": False,
                "error": str(e)
            }

def create_reddit_tool():
    """Create and return a Reddit tool instance"""
    return RedditSearchTool()

def get_reddit_credentials_help():
    """Print help information for getting Reddit API credentials"""
    print("🔧 To get valid Reddit API credentials:")
    print("1. Go to https://www.reddit.com/prefs/apps")
    print("2. Click 'Create App' or 'Create Another App'")
    print("3. Fill in the details:")
    print("   - Name: Your app name (e.g., 'CrewAI Reddit Tool')")
    print("   - App type: Select 'script'")
    print("   - Description: Brief description")
    print("   - About URL: Can be blank")
    print("   - Redirect URI: http://localhost:8080")
    print("4. Click 'Create app'")
    print("5. Copy the Client ID (under your app name)")
    print("6. Copy the Client Secret (labeled 'secret')")
    print("7. Add to your .env file:")
    print("   REDDIT_CLIENT_ID=your_client_id")
    print("   REDDIT_CLIENT_SECRET=your_client_secret")
    print("   REDDIT_USER_AGENT=CrewAI_Reddit_Tool/1.0")

# Example usage
if __name__ == "__main__":
    # Test the Reddit tool
    reddit_tool = RedditSearchTool()
    
    # Test connection
    print("🔧 Testing Reddit connection...")
    connection_status = reddit_tool.test_connection()
    
    if connection_status["status"] == "success":
        print("✅ Reddit connection successful!")
        print(f"Test post: {connection_status.get('test_post', 'N/A')}")
        
        # Test search
        print("\n🔍 Testing Reddit search...")
        results = reddit_tool.search_subreddit("python", "machine learning", limit=3)
        if results and "error" not in results[0]:
            print(f"Found {len(results)} posts")
            for post in results:
                print(f"- {post.get('title', 'No title')} (Score: {post.get('score', 0)})")
        else:
            print(f"❌ Error: {results[0].get('error', 'Unknown error')}")
        
        # Test sentiment analysis
        print("\n📊 Testing sentiment analysis...")
        analysis = reddit_tool.analyze_sentiment("artificial", "AI", limit=5)
        if "error" not in analysis:
            print(f"Analysis completed successfully!")
            print(f"Posts analyzed: {analysis.get('total_posts_analyzed')}")
            print(f"Average score: {analysis.get('average_score')}")
        else:
            print(f"❌ Error: {analysis.get('error')}")
    else:
        print(f"❌ {connection_status['message']}")
        print("\n" + "="*50)
        get_reddit_credentials_help()
        print("="*50)
