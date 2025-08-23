# Pollz API - Bruno Collection

This Bruno collection provides comprehensive API testing capabilities for the Pollz voting platform backend.

## 🚀 Quick Start

### Prerequisites

1. **Install Bruno**: Download from [https://www.usebruno.com/](https://www.usebruno.com/)
2. **Backend Setup**: Ensure the Pollz backend is running via Docker Compose
3. **Authentication**: Obtain valid JWT tokens for authenticated endpoints

### Setup Instructions

1. **Open Collection**: Import this `bruno` folder into Bruno
2. **Select Environment**: Choose between `Development` or `Production`
3. **Configure Tokens**: Set `auth_token` and `refresh_token` in your environment after authentication

## 🏗️ Collection Structure

### Core API Groups

#### 🔐 Authentication
- **Google Login**: Authenticate with Google OAuth ID token
- **Logout**: Invalidate user session
- **User Profile**: Get authenticated user information

#### 🗳️ Elections
- **Get Election Positions**: List all voting positions
- **Get Election Candidates**: List all candidates
- **Get Candidates by Position**: Filter candidates by position
- **Get Live Election Stats**: Real-time voting statistics
- **Cast Anonymous Vote**: Submit vote for candidate
- **Check Vote Status**: Verify user's voting status

#### 📚 Huels (Courses)
- **Get Departments**: List academic departments
- **Get All Huels**: List courses with filtering
- **Get Huel Detail**: Detailed course information
- **Rate Huel**: Submit course ratings
- **Comment on Huel**: Add course comments

#### 🏛️ Departments-Clubs
- **Get Department Clubs**: List available clubs
- **Vote for Department Club**: Submit club votes
- **Comment on Department Club**: Add club comments

#### ⚙️ Voting-Control
- **Get Voting Status by Type**: Check specific voting session status
- **Get All Voting Statuses**: Overview of all voting sessions

#### 📊 Statistics
- **Get Voting Stats**: Comprehensive voting statistics
- **Get Dashboard Stats**: Administrative overview data

#### 🤝 Contributions
- **Get Project Info**: Project metadata
- **Get GitHub Contributors**: Comprehensive contributor data
- **Get GitHub Contributors Basic**: Simplified contributor info
- **Get GitHub Contributors Details**: Detailed contributor profiles
- **Get GitHub Contributors Commits**: Commit statistics
- **Get GitHub Contributors Lines**: Lines of code metrics
- **Debug Contributor**: Troubleshooting endpoint

#### 🔑 JWT-Tokens
- **Obtain Token Pair**: Get access/refresh tokens (username/password)
- **Refresh Token**: Renew expired access token
- **Verify Token**: Validate token status

#### 💬 SuperChat
- **Create Order**: Create Razorpay payment order ⚠️ *Currently Disabled*
- **Razorpay Webhook**: Payment notification handler ⚠️ *Currently Disabled*
- **Get Super Chats**: Retrieve live SuperChat messages ⚠️ *Currently Disabled*

#### 🔧 Legacy-Debug (Remove them please)
- **Legacy GenSec Vote**: Backward compatibility endpoint
- **Legacy President Vote**: Backward compatibility endpoint
- **Legacy Candidate Data**: Backward compatibility endpoint
- **Legacy Total Votes**: Backward compatibility endpoint
- **Sentry Debug**: Error monitoring test endpoint

## 🌍 Environment Configuration

### Development Environment
- **Base URL**: `http://localhost:6969`
- **Usage**: Local development with Docker Compose
- **Setup**: Run `docker-compose up` in the backend directory

### Production Environment
- **Base URL**: `https://pollz.bits-acm.in`
- **Usage**: Live production testing
- **Requirements**: Valid BITS Pilani email domain

## 🔐 Authentication Workflow

### Google OAuth Flow (Recommended)

1. **Frontend OAuth**: Implement Google OAuth in your frontend application
2. **Get ID Token**: Extract the `id_token` from the OAuth response
3. **Backend Login**: Use the "Google Login" endpoint with the ID token
4. **Store Tokens**: Save the returned `access` and `refresh` tokens
5. **Set Environment**: Update Bruno environment variables with tokens

```javascript
// Example: Setting tokens after login
{
  "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Direct JWT Authentication

1. **Obtain Token Pair**: Use username/password with "Obtain Token Pair"
2. **Set Tokens**: Update environment variables with returned tokens
3. **Refresh When Needed**: Use "Refresh Token" endpoint for expired tokens

## 📱 Common Testing Workflows

### Complete Voting Workflow

1. **Authentication**: Login using Google OAuth
2. **Check Voting Status**: Verify voting sessions are active
3. **Get Positions**: List available election positions
4. **Get Candidates**: View candidates for each position
5. **Cast Vote**: Submit anonymous votes for candidates
6. **Verify Vote**: Confirm vote was recorded
7. **View Stats**: Check real-time voting statistics

### Course Rating Workflow

1. **Authentication**: Ensure user is authenticated
2. **Get Departments**: List available departments
3. **Get Huels**: Browse courses (optionally filter by department)
4. **Get Huel Detail**: View detailed course information
5. **Rate Huel**: Submit difficulty/quality/usefulness ratings
6. **Comment on Huel**: Add text feedback

### Club Voting Workflow

1. **Authentication**: Ensure user is authenticated
2. **Check Voting Status**: Verify club voting is active
3. **Get Department Clubs**: List available clubs
4. **Vote for Club**: Submit upvote/downvote
5. **Comment on Club**: Add club feedback

## 🛠️ Development Tips

### Token Management
- Tokens expire periodically - use the "Verify Token" endpoint to check validity
- Refresh tokens before they expire using the "Refresh Token" endpoint
- Store tokens securely and never commit them to version control

### Error Handling
- Most endpoints return standard HTTP status codes
- Authentication errors typically return `401 Unauthorized`
- Permission errors return `403 Forbidden`
- Validation errors return `400 Bad Request` with detailed messages

### Testing Best Practices
1. **Start with Authentication**: Always authenticate before testing protected endpoints
2. **Check Voting Status**: Verify voting sessions are active before testing voting endpoints
3. **Use Real Data**: Test with realistic data that matches your application's requirements
4. **Test Error Scenarios**: Try invalid requests to understand error responses

## 🚦 Endpoint Status Reference

- ✅ **Active**: Fully functional and ready for use
- ⚠️ **Disabled**: Currently disabled in backend (SuperChat endpoints)
- 🔄 **Legacy**: Maintained for backward compatibility, use newer alternatives
- 🧪 **Debug**: Development/testing purposes only

## 🆘 Troubleshooting

### Common Issues

#### Authentication Failures
- **Issue**: `401 Unauthorized` on authenticated endpoints
- **Solution**: Verify `auth_token` is set correctly in environment
- **Check**: Use "Verify Token" endpoint to confirm token validity

#### CORS Errors
- **Issue**: Browser blocks requests from different origin
- **Solution**: Ensure backend CORS settings allow your domain
- **Development**: Use backend's Docker setup on port 6969

#### Invalid Tokens
- **Issue**: Tokens appear invalid or expired
- **Solution**: Use "Refresh Token" endpoint to get new access token
- **Alternative**: Re-authenticate using Google Login

#### Domain Restrictions
- **Issue**: Google login fails with domain error
- **Solution**: Ensure using BITS Pilani email domain (@pilani.bits-pilani.ac.in)
- **Check**: Verify email domain in authentication response

### Support

For technical issues or questions:
1. Check the backend logs when running Docker Compose
2. Use the "Sentry Debug" endpoint to test error tracking
3. Review the Django backend source code for detailed API behavior
4. Consult the project's GitHub repository for additional documentation

## 📄 API Documentation

This Bruno collection serves as interactive API documentation. Each request includes:
- **Purpose**: What the endpoint does
- **Requirements**: Authentication and permission needs
- **Parameters**: URL parameters, query strings, and request body format
- **Usage Notes**: Special considerations and best practices

For detailed backend implementation, refer to the Django views and serializers in the source code.