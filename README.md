# SIGHT-SYSTEMs - Unified Manufacturing Management Platform

A comprehensive manufacturing management system consisting of three integrated applications for bot assembly, machine shop operations, and unified access control.

## 🏗️ System Architecture

```
SIGHT-SYSTEMs/
├── BOTSIGHT/          # Bot Assembly & Quality Management (Port 5000 - HTTPS)
├── CHIPSIGHT/         # Digital Twin for Manufacturing (Port 5001 - HTTP)
├── plant_union/       # Landing Page & SSO Gateway (Port 5002 - HTTP)
├── run.py            # Unified Launcher (Multiprocessing)
├── run_simple.py     # Simple Unified Launcher (Threading)
├── start_sight_systems.bat  # Windows Batch Launcher
└── start_sight_systems.ps1  # PowerShell Launcher
```

## 🚀 Quick Start

### Option 1: Windows Batch File (Recommended)
```bash
# Double-click or run from command line
start_sight_systems.bat
```

### Option 2: PowerShell Script (Windows)
```powershell
# Right-click and "Run with PowerShell" or run from command line
.\start_sight_systems.ps1
```

### Option 3: Simple Python Launcher (Recommended for troubleshooting)
```bash
# Install dependencies first
pip install -r requirements.txt

# Start all applications using threading (more reliable)
python run_simple.py
```

### Option 4: Advanced Python Launcher (Multiprocessing)
```bash
# Install dependencies first
pip install -r requirements.txt

# Start all applications using multiprocessing
python run.py
```

### Option 5: Individual Applications
```bash
# BOTSIGHT (Bot Assembly)
cd BOTSIGHT
python run_eventlet.py

# CHIPSIGHT (Digital Twin)
cd CHIPSIGHT
python run.py

# PLANT_UNION (Landing Page)
cd plant_union
python app.py
```

## 🌐 Access URLs

Once started, access the applications at:

- **PLANT_UNION (Landing Page)**: http://localhost:5002
- **BOTSIGHT (Bot Assembly)**: https://localhost:5000
- **CHIPSIGHT (Digital Twin)**: http://localhost:5001

## 📋 System Components

### 1. BOTSIGHT - Bot Assembly & Quality Management
- **Purpose**: Manages bot assembly lines and quality control
- **Features**:
  - Multi-role access (Operator, Quality, Dispatch, Testing, Manager, Planner, Plant Head)
  - QR code scanning for bot tracking
  - Real-time assembly line monitoring
  - Quality inspection workflows
  - Daily production reports
  - Bot finder and search capabilities

### 2. CHIPSIGHT - Digital Twin for Manufacturing
- **Purpose**: Comprehensive digital twin for CNC/VMC machine operations
- **Features**:
  - Multi-role dashboard system
  - Real-time machine monitoring and OEE calculations
  - Quality control with FPI/LPI inspections
  - Production planning with Excel uploads
  - Drawing management and SAP integration
  - Rework queue management
  - Machine breakdown tracking
  - Route management and transfer operations

### 3. PLANT_UNION - Landing Page & SSO Gateway
- **Purpose**: Unified entry point with system selection and SSO capabilities
- **Features**:
  - Landing page with system selection
  - Auto-login functionality
  - SSO token generation
  - Redirects to appropriate applications

## 🔧 Prerequisites

- Python 3.8 or higher
- Windows 10/11 (for batch file and PowerShell script)
- Internet connection for initial dependency installation

## 📦 Installation

1. **Clone or download** the SIGHT-SYSTEMs repository
2. **Navigate** to the root directory
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Generate SSL certificates** (for BOTSIGHT HTTPS):
   - The system will automatically generate certificates using mkcert.exe
   - If mkcert.exe is not available, you'll need to generate certificates manually

## 🔐 Default Login Credentials

### BOTSIGHT
- **Planner**: planner/plannerpass
- **Manager**: manager/managerpass
- **Quality**: quality/qualitypass
- **Operator**: Use operator login panel

### CHIPSIGHT
- **Admin**: admin/adminpass
- **Plant Head**: plant_head/plantpass
- **Planner**: planner/plannerpass
- **Manager**: manager/managerpass
- **Quality**: quality/qualitypass
- **Operator**: Use operator login panel

## 🛠️ Configuration

### Port Configuration
The unified launcher uses the following ports:
- **5000**: BOTSIGHT (HTTPS)
- **5001**: CHIPSIGHT (HTTP)
- **5002**: PLANT_UNION (HTTP)

To change ports, edit the `APPS` configuration in `run.py` or `run_simple.py`.

### SSL Certificates
BOTSIGHT requires SSL certificates for HTTPS. The system will:
1. Check for existing certificates (`localhost.pem` and `localhost-key.pem`)
2. Generate new certificates using `mkcert.exe` if not found
3. Fall back to HTTP if certificates cannot be generated

## 📊 Monitoring

### Logs
- **Unified Launcher**: `logs/unified_launcher.log`
- **BOTSIGHT**: `BOTSIGHT/logs/` (if any)
- **CHIPSIGHT**: `CHIPSIGHT/logs/`

### Process Management
The unified launcher:
- Starts all applications in separate processes/threads
- Monitors process health
- Gracefully shuts down all applications on Ctrl+C
- Cleans up ports on exit

## 🔄 Troubleshooting

### Common Issues

1. **Unicode Encoding Errors (Windows)**
   - **Solution**: Use `run_simple.py` instead of `run.py`
   - **Cause**: Windows console doesn't support emoji characters in logging
   - **Alternative**: Use PowerShell script `start_sight_systems.ps1`

2. **Port Already in Use**
   - The launcher will automatically attempt to kill processes using required ports
   - If manual intervention is needed, use Task Manager to end Python processes

3. **SSL Certificate Issues**
   - Ensure `mkcert.exe` is present in the BOTSIGHT directory
   - Or manually generate certificates for localhost

4. **Directory Path Issues (Multiprocessing)**
   - **Solution**: Use `run_simple.py` (threading) instead of `run.py` (multiprocessing)
   - **Cause**: Multiprocessing can have issues with directory changes on Windows

5. **Database Issues**
   - CHIPSIGHT will automatically initialize its database if not present
   - BOTSIGHT uses SQLite and will create the database automatically

6. **Dependency Issues**
   - Ensure all requirements are installed: `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

### Launcher Comparison

| Feature | `run.py` (Multiprocessing) | `run_simple.py` (Threading) |
|---------|---------------------------|----------------------------|
| **Process Isolation** | ✅ Full isolation | ⚠️ Shared memory space |
| **Windows Compatibility** | ⚠️ Directory issues | ✅ Better compatibility |
| **Unicode Support** | ⚠️ Encoding issues | ✅ Better support |
| **Resource Usage** | ✅ Lower memory usage | ⚠️ Higher memory usage |
| **Stability** | ⚠️ Can have issues | ✅ More stable |

**Recommendation**: Use `run_simple.py` for better Windows compatibility.

### Manual Startup
If the unified launcher fails, you can start applications individually:

```bash
# Terminal 1 - BOTSIGHT
cd BOTSIGHT
python run_eventlet.py

# Terminal 2 - CHIPSIGHT
cd CHIPSIGHT
python run.py

# Terminal 3 - PLANT_UNION
cd plant_union
python app.py
```

## 📞 Support

For technical support and inquiries:
- Check the logs in the `logs/` directory
- Review individual application documentation in their respective folders
- Contact system administrator

## 📄 License

Copyright © 2025 Diwakar Singh. All rights reserved.
See individual application license files for specific terms.

---

**Note**: This is a production-ready manufacturing management system. Ensure proper backup procedures are in place before deployment. 