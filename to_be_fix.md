# To Be Fixed - AiThena Issues

## Current Issues

### 1. Streamlit Page Navigation Error
**Error**: `StreamlitAPIException: Could not find page: 'pages/2_Dashboard'`
**Location**: `frontend/pages/1_Sign_in.py` line 16
**Description**: When running Streamlit from project root, page navigation paths are incorrect
**Current Code**: `st.switch_page("pages/2_Dashboard")`
**Issue**: The path should be relative to the frontend directory, not include "pages/" prefix

**Fix Needed**: 
- Change `st.switch_page("pages/2_Dashboard")` to `st.switch_page("2_Dashboard")`
- Apply similar fixes to all page navigation calls

### 2. Deprecated Streamlit Functions
**Error**: `AttributeError: module 'streamlit' has no attribute 'experimental_rerun'`
**Status**: ✅ FIXED - Replaced with `st.rerun()`
**Files Updated**: 
- `frontend/pages/1_Sign_in.py`
- `frontend/pages/2_Dashboard.py`

### 3. Logo Path Issue
**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'assets/logo.png'`
**Status**: ✅ FIXED - Updated path to `frontend/assets/logo.png`
**File Updated**: `frontend/Home.py`

## Pending Fixes

### 4. Page Navigation Consistency
**Issue**: Need to update all page navigation calls to use correct relative paths
**Files to Check**:
- All files in `frontend/pages/` directory
- Look for `st.switch_page()` and `st.page_link()` calls

### 5. Environment Variable Validation
**Issue**: Ensure all required environment variables are properly validated
**Files to Check**:
- `backend/granite.py`
- `backend/auth.py`
- `backend/main.py`

## Testing Checklist

- [ ] User registration and login
- [ ] Page navigation between all pages
- [ ] YouTube transcript extraction
- [ ] AI summarization functionality
- [ ] Flashcard generation
- [ ] Quiz generation
- [ ] Adaptive feedback
- [ ] Logout functionality

## Notes

- Running Streamlit from project root (`streamlit run frontend/Home.py`) requires different path handling than running from frontend directory
- All page navigation should be relative to the frontend directory structure
- Environment variables must be properly set in `.env` file
