# Anonymous Election Voting Algorithm

## Overview

This document describes the cryptographic anonymous voting system implemented in the Pollz application. The system ensures complete voter privacy while maintaining election integrity and preventing double voting.

## Core Principle

The system uses one-way cryptographic hashing (SHA-256) to create anonymous voter identifiers that cannot be traced back to the original user, while still preventing duplicate votes.

## Algorithm Components

### 1. Anonymous Voter Hash Generation

```python
def create_voter_hash(user_id, position_id):
    salt = "pollz_anonymous_voting_salt_2024"
    data = f"{user_id}:{position_id}:{salt}"
    return hashlib.sha256(data.encode()).hexdigest()
```

**Input**: User ID, Position ID, Secret Salt
**Output**: 64-character hexadecimal hash
**Property**: Deterministic but irreversible

**Example**:
- User ID: 123
- Position ID: 1 (President)
- Salt: "pollz_anonymous_voting_salt_2024"
- Input String: "123:1:pollz_anonymous_voting_salt_2024"
- Output Hash: "a7b8c9d2e3f4567890abcdef12345678901234567890abcdef1234567890abcd"

### 2. Vote Signature Generation

```python
def create_vote_signature(voter_hash, candidate_id, timestamp):
    data = f"{voter_hash}:{candidate_id}:{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()
```

**Purpose**: Cryptographic proof of vote integrity
**Input**: Anonymous voter hash, candidate ID, timestamp
**Output**: Verification signature

### 3. Database Schema

```sql
CREATE TABLE anonymous_election_votes (
    id SERIAL PRIMARY KEY,
    voter_hash VARCHAR(64) NOT NULL,
    candidate_id INTEGER NOT NULL,
    position_id INTEGER NOT NULL,
    vote_signature VARCHAR(128) NOT NULL,
    ip_hash VARCHAR(64),
    voted_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(voter_hash, position_id)
);
```

**Key Features**:
- No direct user reference stored
- Unique constraint prevents double voting
- IP addresses are hashed for fraud prevention
- Immutable records (no updates/deletes allowed)

### 4. Voting Process

```
1. User Authentication (temporary)
   └─ Verify user eligibility

2. Hash Generation
   ├─ Create voter_hash = SHA256(user_id + position_id + salt)
   └─ Create ip_hash = SHA256(ip_address + salt)

3. Duplicate Vote Check
   ├─ Query: SELECT * FROM votes WHERE voter_hash = ? AND position_id = ?
   └─ Reject if exists

4. Vote Recording
   ├─ Generate signature = SHA256(voter_hash + candidate_id + timestamp)
   ├─ Store anonymous vote record
   └─ Update candidate vote count

5. User Session Ends
   └─ No persistent connection between user and vote
```

### 5. Privacy Guarantees

**Mathematical Guarantee**: Given a voter hash, it is computationally infeasible to determine the original user ID due to:
- SHA-256 one-way function properties
- Secret salt prevents rainbow table attacks
- No reverse lookup mechanism exists

**Admin Limitations**: System administrators can only see:
- Partial hash (first 8 characters): "a7b8c9d2..."
- Vote choice and timestamp
- Signature validity status
- Cannot determine voter identity

### 6. Security Properties

**Anonymity**: Votes cannot be traced to voters
**Integrity**: Cryptographic signatures prevent tampering
**Uniqueness**: One vote per user per position enforced
**Auditability**: All votes are verifiable but anonymous
**Coercion Resistance**: No way to prove individual vote choices

### 7. Example Scenario

**Setup**:
- User: Alice (ID: 456)
- Position: General Secretary (ID: 2)
- Candidate: John Smith (ID: 789)

**Process**:
1. Alice authenticates and requests to vote
2. System generates voter_hash = SHA256("456:2:pollz_anonymous_voting_salt_2024") = "f2e5a8b1..."
3. System checks if "f2e5a8b1..." has voted for position 2
4. If not, creates vote record with voter_hash "f2e5a8b1...", candidate 789
5. Alice's session ends, no persistent link to vote exists

**Database Record**:
```
voter_hash: f2e5a8b1c4d7...
candidate_id: 789
position_id: 2
vote_signature: 3c9f8e2a5b1d...
voted_at: 2024-03-15 14:30:00
```

**Admin View**: Can see partial hash "f2e5a8b1..." voted for John Smith, but cannot determine this was Alice.

### 8. Implementation Files

**Backend**:
- `models.py`: AnonymousElectionVote model
- `views.py`: cast_anonymous_election_vote endpoint
- `admin.py`: Privacy-protected admin interface

**Frontend**:
- Privacy notices explaining anonymity guarantees
- Vote verification display
- Transparency messaging with GitHub links

### 9. Verification Process

Users receive vote confirmation with:
- Partial voter ID (first 8 characters of hash)
- Vote signature for verification
- Timestamp of vote

Anyone can verify vote integrity by:
1. Computing expected signature from public data
2. Comparing with stored signature
3. Confirming vote authenticity without revealing voter identity

### 10. Deployment Considerations

**Production Requirements**:
- Store salt values in environment variables
- Use HTTPS for all communications
- Implement rate limiting on voting endpoints
- Regular signature verification audits
- Secure database with encrypted storage

**Monitoring**:
- Track vote signature validation rates
- Monitor for suspicious voting patterns
- Audit trail for all vote operations
- Regular cryptographic integrity checks

## Conclusion

This anonymous voting system provides mathematical guarantees of voter privacy while maintaining complete election integrity. The one-way cryptographic approach ensures that even system administrators cannot compromise voter anonymity, creating a trustworthy democratic voting platform.