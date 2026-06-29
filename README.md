# Risk Management System

A full-stack web application for organization-wide risk management, enabling department-wise risk creation, tracking, monitoring, and analytics.

## Features

- **Risk Register Management**: Create, update, and delete risks with full FMEA (Failure Mode and Effects Analysis) support
- **RPN Calculation**: Automatic Risk Priority Number calculation (Severity × Occurrence × Detection)
- **Risk Thresholding**: Automatic classification of high-risk items (RPN >= 27)
- **Action Tracking**: Preventive and mitigation action management with status tracking
- **Review System**: Periodic risk reviews with RPN trend analysis
- **Dashboard Analytics**: Interactive charts and metrics visualization
- **Role-Based Access Control**: Admin and department user roles
- **Department Isolation**: Department users see only their department's risks
- **Audit Trail**: Complete audit logging for all risk modifications

## Technology Stack

### Backend
- Node.js with Express.js
- MySQL database
- JWT authentication
- bcryptjs for password hashing

### Frontend
- React 18
- React Router for navigation
- Recharts for data visualization
- Axios for API communication

## Database Schema

### Tables

1. **departments**: Organization departments
2. **users**: System users with role-based access
3. **risks**: Master risk register with RPN calculation
4. **risk_reviews**: Periodic risk reviews
5. **actions**: Preventive and mitigation actions
6. **audit_logs**: Complete audit trail

## Installation

### Prerequisites

- Node.js (v14 or higher)
- MySQL (v5.7 or higher)
- npm or yarn

### 1. Clone the repository

```bash
git clone <repository-url>
cd risk-management-system
```

### 2. Database Setup

Create a MySQL database:

```sql
CREATE DATABASE risk_management;
```

Run the schema and seed data:

```bash
mysql -u root -p risk_management < database/schema.sql
mysql -u root -p risk_management < database/seed-data.sql
```

### 3. Backend Setup

```bash
cd backend
npm install
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
PORT=5000
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=risk_management
JWT_SECRET=your-secret-key-change-this-in-production
NODE_ENV=development
```

Start the backend server:

```bash
npm run dev
```

### 4. Frontend Setup

In a new terminal:

```bash
cd frontend
npm install
cp .env.example .env
```

Start the frontend development server:

```bash
npm start
```

The application will be available at `http://localhost:3000`

## Demo Credentials

The seed data includes the following users (passwords need to be hashed):

**Note**: You'll need to update the password hashes in the seed data with actual bcrypt hashes. Use:

```javascript
const bcrypt = require('bcryptjs');
console.log(bcrypt.hashSync('your_password', 10));
```

Example users in seed-data.sql:
- **Admin**: `admin / admin123`
- **Finance User**: `finance_user / finance123`
- **IT User**: `it_user / it123`
- **HR User**: `hr_user / hr123`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Risks
- `GET /api/risks` - Get all risks (filtered by department)
- `GET /api/risks/:id` - Get risk by ID
- `POST /api/risks` - Create new risk
- `PUT /api/risks/:id` - Update risk
- `DELETE /api/risks/:id` - Delete risk
- `POST /api/risks/:id/reviews` - Add risk review
- `GET /api/risks/:id/reviews` - Get risk reviews

### Actions
- `GET /api/actions/risk/:risk_id` - Get actions for a risk
- `POST /api/actions/risk/:risk_id` - Create action
- `PUT /api/actions/:id` - Update action
- `DELETE /api/actions/:id` - Delete action
- `GET /api/actions/overdue` - Get overdue actions

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/departments` - Get all departments

## Business Rules

### RPN Calculation
- RPN = Severity × Occurrence × Detection
- Severity, Occurrence, Detection are rated on a scale of 1-10

### Risk Threshold
- RPN >= 27: Risk is classified as "Tracked / Monitored"
- RPN < 27: Risk is classified as "Not Tracked"

### Review Frequency
- Monthly or quarterly reviews should be conducted for tracked risks

### Audit Requirements
- All risk updates are logged with:
  - User who made the change
  - Timestamp
  - Old and new values
  - IP address

## Project Structure

```
risk-management-system/
├── backend/
│   ├── config/
│   │   └── database.js         # Database configuration
│   ├── controllers/
│   │   ├── authController.js   # Authentication logic
│   │   ├── riskController.js   # Risk CRUD operations
│   │   ├── actionController.js # Action management
│   │   └── dashboardController.js # Dashboard analytics
│   ├── middleware/
│   │   ├── auth.js             # JWT authentication
│   │   └── audit.js            # Audit logging
│   ├── routes/
│   │   ├── authRoutes.js       # Auth endpoints
│   │   ├── riskRoutes.js       # Risk endpoints
│   │   ├── actionRoutes.js     # Action endpoints
│   │   └── dashboardRoutes.js  # Dashboard endpoints
│   ├── server.js               # Main server file
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx # Authentication context
│   │   ├── pages/
│   │   │   ├── Login.jsx       # Login page
│   │   │   ├── Dashboard.jsx   # Dashboard with charts
│   │   │   ├── RiskList.jsx    # Risk register list
│   │   │   ├── RiskForm.jsx    # Create/Edit risk form
│   │   │   └── RiskDetail.jsx  # Risk details and actions
│   │   ├── services/
│   │   │   └── api.js          # API service layer
│   │   ├── App.jsx             # Main app with routing
│   │   └── index.js            # Entry point
│   ├── package.json
│   └── .env.example
├── database/
│   ├── schema.sql              # Database schema
│   └── seed-data.sql           # Sample data
└── README.md
```

## Sample API Payloads

### Create Risk

```json
{
  "department_id": 1,
  "process_function": "Payroll Processing",
  "risk_description": "Payroll calculation errors leading to incorrect payments",
  "potential_failure_mode": "Incorrect tax withholding calculation",
  "potential_effects": "Employee dissatisfaction, legal penalties",
  "severity": 8,
  "potential_causes": "Outdated tax tables, manual calculation errors",
  "current_controls_prevention": "Automated tax calculation system",
  "occurrence": 6,
  "current_controls_detection": "Monthly payroll audits",
  "detection": 4,
  "recommended_actions": "Implement automated tax table updates"
}
```

### Create Action

```json
{
  "action_type": "preventive",
  "action_description": "Review and update tax tables quarterly",
  "action_owner": "Finance Manager",
  "due_date": "2026-02-28"
}
```

### Create Risk Review

```json
{
  "review_date": "2026-01-15",
  "severity": 7,
  "occurrence": 4,
  "detection": 3,
  "notes": "Controls improved, risk reduced"
}
```

## Security Considerations

1. **JWT Secret**: Change `JWT_SECRET` in production
2. **Database Password**: Use strong database passwords
3. **HTTPS**: Enable HTTPS in production
4. **Rate Limiting**: Implement rate limiting for API endpoints
5. **Input Validation**: All inputs are validated on both client and server
6. **SQL Injection Prevention**: Parameterized queries are used throughout

## Development

### Running Tests

```bash
cd backend
npm test
```

### Building for Production

```bash
cd frontend
npm run build
```

The built files will be in the `frontend/build` directory.

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in `.env` file
- Ensure database exists

### CORS Issues
- Check `origin` in CORS configuration in `server.js`
- Ensure frontend URL is allowed

### Authentication Issues
- Verify JWT_SECRET matches between backend and any validation
- Check token expiration time
- Clear browser local storage if needed

## Future Enhancements

- Email notifications for overdue actions
- PDF export of risk register
- Advanced filtering and search
- Role-based dashboards
- Multi-language support
- Integration with external systems (SAP, etc.)
- Mobile-responsive design improvements
- Real-time updates with WebSockets

## License

ISC

## Support

For issues and questions, please create an issue in the repository.
