# 🚀 CrewAI + IBM Watson Setup Guide

## ✅ **Current Status: CONFIGURED & WORKING**

Your CrewAI project is now properly configured to use IBM Watson API keys! Here's what's been set up:

## 📋 **What's Configured**

### **1. Environment Variables (.env)**
```bash
MODEL=watsonx/meta-llama/llama-3-2-1b-instruct
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_APIKEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
```

### **2. CrewAI Configuration (crew.py)**
- ✅ Added `_get_watson_llm()` method
- ✅ Configured all agents to use Watson LLM
- ✅ Set proper model parameters
- ✅ Added environment variable loading

### **3. Model Configuration**
- **Model**: `watsonx/meta-llama/llama-3-2-1b-instruct`
- **Temperature**: 0.7
- **Max Tokens**: 512
- **Top P**: 0.9
- **Top K**: 50
- **Repetition Penalty**: 1.1

## 🎯 **How It Works**

### **Step 1: Environment Loading**
```python
import os
from dotenv import load_dotenv
load_dotenv()  # Loads .env file
```

### **Step 2: Watson LLM Configuration**
```python
def _get_watson_llm(self) -> LLM:
    api_key = os.getenv("WATSONX_APIKEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    model = os.getenv("MODEL", "watsonx/meta-llama/llama-3-2-1b-instruct")
    
    return LLM(
        model=model,
        config={
            "api_key": api_key,
            "project_id": project_id,
            "url": url,
            "temperature": 0.7,
            "max_tokens": 512,
            # ... other parameters
        }
    )
```

### **Step 3: Agent Assignment**
```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        llm=self._get_watson_llm(),  # ← Watson LLM assigned here
        verbose=True
    )
```

## 🧪 **Testing Your Setup**

### **Run Configuration Test**
```bash
source .venv/bin/activate && python test_watson_config.py
```

### **Run Diagnostic**
```bash
source .venv/bin/activate && python llm_diagnostic.py
```

### **Run Your Crew**
```bash
source .venv/bin/activate && python -m techxchange_hackathon_neuralnexis.main
```

## 🔧 **Customization Options**

### **Change Model**
Edit your `.env` file:
```bash
MODEL=watsonx/meta-llama/llama-3.1-8b-instruct  # Different model
```

### **Adjust Parameters**
Edit `crew.py` in the `_get_watson_llm()` method:
```python
config={
    "temperature": 0.5,      # More focused
    "max_tokens": 1024,      # Longer responses
    "top_p": 0.8,           # More diverse
    # ... other parameters
}
```

### **Add More Models**
You can create different LLM configurations:
```python
def _get_watson_llm_creative(self) -> LLM:
    # Higher temperature for creative tasks
    return LLM(model="watsonx/meta-llama/llama-3.1-8b-instruct", 
               config={"temperature": 0.9, ...})

def _get_watson_llm_precise(self) -> LLM:
    # Lower temperature for precise tasks
    return LLM(model="watsonx/meta-llama/llama-3.2-1b-instruct", 
               config={"temperature": 0.3, ...})
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **"API Key Not Found"**
   - Check your `.env` file exists
   - Verify `WATSONX_APIKEY` is set correctly
   - No spaces around `=` in `.env`

2. **"Project ID Not Found"**
   - Verify `WATSONX_PROJECT_ID` in `.env`
   - Check for trailing characters (like `%`)

3. **"API Connection Failed"**
   - Verify API key permissions in IBM Watson Studio
   - Check if project is a Watson AI project (not classic Watson)
   - Ensure you have credits/quota available

4. **"Model Not Found"**
   - Check model name spelling
   - Verify model is available in your Watson project
   - Try a different model from the catalog

### **Debug Commands**
```bash
# Check environment variables
source .venv/bin/activate && python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', 'Set' if os.getenv('WATSONX_APIKEY') else 'Not set')"

# Test Watson connection
source .venv/bin/activate && python test_watson_config.py

# Run diagnostic
source .venv/bin/activate && python llm_diagnostic.py
```

## 📚 **Available Models**

### **Llama Models**
- `watsonx/meta-llama/llama-3.2-1b-instruct` (current)
- `watsonx/meta-llama/llama-3.1-8b-instruct`
- `watsonx/meta-llama/llama-3.1-70b-instruct`

### **Granite Models**
- `ibm/granite-13b-instruct-v2`
- `ibm/granite-20b-instruct-v2`

### **Code Models**
- `ibm/granite-13b-code-instruct-v2`
- `ibm/granite-20b-code-instruct-v2`

## 🎉 **Success Indicators**

✅ **Environment variables loaded correctly**
✅ **CrewAI agents created with Watson LLM**
✅ **API connection successful**
✅ **Text generation working**
✅ **All agents using same Watson configuration**

## 🚀 **Next Steps**

1. **Test your crew**: Run the main application
2. **Monitor usage**: Check Watson Studio for API calls
3. **Optimize**: Adjust parameters based on results
4. **Scale**: Add more agents or different models

---

**Your CrewAI project is now fully configured with IBM Watson! 🎯✨**
