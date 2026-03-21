# Znova Development Guide

Znova is a high-performance, Odoo-inspired full-stack framework designed for rapid business application development. It utilizes a FastAPI backend with an automated "Recordset" ORM and a Vue.js 3 frontend that auto-generates UI from model metadata.

## 🏗️ Architecture Overview

- **Backend**: FastAPI (Python 3.10+)
  - **ORM**: Znova ORM (SQLAlchemy-based) with Odoo-style `Environment` and `Recordset`.
  - **Data Loading**: Directory-based seeding with symbolic reference support.
  - **Real-time**: Integrated WebSocket manager for live push notifications.
- **Frontend**: Vue.js 3 + Vite + TailwindCSS
  - **Dynamic UI**: Generic components render specialized views (List, Form, Kanban) based on backend metadata.
  - **Auth**: Secure JWT-based authentication with role-aware routing.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+, Node.js 18+, PostgreSQL.

### Setup Commands

1. **Initialize Backend**:
   ```bash
   cd backend && python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Initialize Frontend**:
   ```bash
   cd frontend && npm install
   ```
3. **Database Setup**:
   Copy `.env.example` to `.env`, set your `DATABASE_URL`, and run:

   ```bash
   # Reset DB and load core data
   python setup_fresh.py

   # Reset DB and load core + demo data
   python setup_fresh.py --demo
   ```

---

## 📦 Znova ORM (`ZnovaModel`)

Models in Znova are defined in `backend/models/`. You define high-level `fields` which the framework uses to generate the database schema and the frontend UI.

### Model Definition Pattern

```python
from backend.core.znova_model import ZnovaModel
from backend.core import fields

class Project(ZnovaModel):
    __tablename__ = "projects"
    _model_name_ = "project"  # Access via env['project']
    _name_field_ = "name"    # Used for display in many2one references

    name = fields.Char(label="Project Name", required=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("active", "Active"),
        ("done", "Done")
    ], label="Status", default="draft")

    user_id = fields.Many2one("user", label="Project Manager")
    task_ids = fields.One2many("project.task", "project_id", label="Tasks")
```

### Available Field Types

Znova provides a comprehensive set of field types that automatically generate both database columns and UI components:

#### Basic Fields

- **`Char(label, size=255, required=False)`**: Single-line text input
  ```python
  name = fields.Char(label="Name", required=True, size=100)
  ```

- **`Text(label, required=False)`**: Multi-line text area
  ```python
  description = fields.Text(label="Description")
  ```

- **`Integer(label, required=False)`**: Numeric integer input
  ```python
  quantity = fields.Integer(label="Quantity", default=0)
  ```

- **`Boolean(label, default=False)`**: Checkbox toggle
  ```python
  active = fields.Boolean(label="Active", default=True)
  ```

- **`Date(label, required=False)`**: Date picker
  ```python
  start_date = fields.Date(label="Start Date")
  ```

- **`DateTime(label, required=False)`**: Date and time picker
  ```python
  created_at = fields.DateTime(label="Created At")
  ```

#### Selection Fields

- **`Selection(options, label, default=None, options={})`**: Dropdown with predefined choices
  ```python
  # Basic selection
  status = fields.Selection([
      ('draft', 'Draft'),
      ('confirmed', 'Confirmed'),
      ('done', 'Done')
  ], label="Status", default='draft')
  
  # Selection with colors (for list view badges)
  status = fields.Selection([
      ('draft', 'Draft'),
      ('live', 'Live'),
      ('done', 'Done')
  ], label="Status", default='draft', options={
      'draft': {'label': 'Draft', 'color': 'info'},
      'live': {'label': 'Live', 'color': 'success'},
      'done': {'label': 'Done', 'color': 'secondary'}
  })
  # Available colors: success, danger, warning, primary, info, secondary, default
  ```

#### Relational Fields

- **`Many2one(relation, label, domain=None)`**: Foreign key relationship
  ```python
  user_id = fields.Many2one("user", label="Assigned To")
  
  # With domain filter
  manager_id = fields.Many2one("user", label="Manager", 
                               domain=[("role.name", "=", "manager")])
  ```

- **`One2many(relation, inverse_field, label, columns=[])`**: Reverse foreign key (list of related records)
  ```python
  task_ids = fields.One2many("project.task", "project_id", label="Tasks",
                            columns=["name", "status", "assigned_to"])
  ```

- **`Many2many(relation, relation_table, column1, column2, label)`**: Many-to-many relationship
  ```python
  tag_ids = fields.Many2many("project.tag", "project_tag_rel", 
                            "project_id", "tag_id", label="Tags")
  ```

#### Media Fields

- **`Image(label, max_size=5242880, allowed_formats=[])`**: Image upload with preview
  ```python
  profile_picture = fields.Image(label="Profile Picture",
                                max_size=5242880,  # 5MB
                                allowed_formats=['jpg', 'png', 'webp'])
  ```

- **`Attachment(label, max_size=10485760, allowed_types=[])`**: Single file attachment
  ```python
  contract = fields.Attachment(label="Contract Document",
                               allowed_types=['pdf', 'doc', 'docx'],
                               max_size=5242880)  # 5MB
  ```

- **`Attachments(label, max_size=10485760, allowed_types=[], max_files=None)`**: Multiple file attachments
  ```python
  documents = fields.Attachments(label="Supporting Documents",
                                allowed_types=['pdf', 'jpg', 'png', 'doc'],
                                max_size=10485760,  # 10MB per file
                                max_files=10)
  ```

#### Special Fields

- **`JSON(label)`**: Store JSON data
  ```python
  metadata = fields.JSON(label="Metadata")
  ```

#### Field Parameters

All fields support these common parameters:

- `label`: Display label in UI
- `required`: Make field mandatory (can be domain string)
- `readonly`: Make field read-only (can be domain string)
- `invisible`: Hide field (can be domain string)
- `default`: Default value
- `help`: Tooltip text
- `domain`: Filter options (for relational fields)
- `widget`: Custom widget type
- `compute`: Method name for computed fields
- `store`: Store computed field value (default: True)

### The Environment API (`self.env`)

Znova uses an Odoo-style environment to manage database sessions and model access.

- **Accessing Models**: `env['model.name']` returns an empty recordset of that model.
- **Searching**: `env['model.name'].search([('field', '=', value)])` returns a recordset of matches.
- **Browsing**: `env['model.name'].browse(ids)` returns a recordset for specific IDs.

### recordset Operations

- **Read**: Access fields directly: `print(project.name)`
- **Write**: `project.write({'name': 'New Name'})` (Handles sessions automatically).
- **Create**: `env['project'].create({'name': 'My project'})`.
- **Delete**: `project.unlink()`.

---

## 📂 Data Loading System

Data is managed in `backend/data/` (mandatory) and `backend/demo/` (optional).

### Record Syntax (`RECORDS`)

Data files are Python modules containing a `RECORDS` dictionary with symbolic XML-IDs:

```python
RECORDS = {
    "role_manager": {
        "model": "role",
        "values": {"name": "manager", "description": "Project Manager"}
    },
    "user_pm": {
        "model": "user",
        "values": {
            "full_name": "Project Manager",
            "email": "pm@example.com",
            "role_id": "@role_manager",  # Link via symbolic ID
            "hashed_password": "$P$secret123" # Magic hash prefix
        }
    }
}
```

---

## 🔐 Permissions & UI View

### Role Permissions

Defined inside the model to control CRUD access per role:

```python
_role_permissions = {
    "admin": {"create": True, "read": True, "write": True, "delete": True, "domain": []},
    "user": {"create": True, "read": True, "write": True, "delete": False, "domain": [("user_id", "=", "user.id")]}
}
```

### UI Views (`_ui_views`)

Controls list and form field visibility, grouping, and specific behavior:

```python
_ui_views = {
    "list": {"fields": ["name", "state", "user_id"]},
    "form": {
        "groups": [
            {"title": "Information", "fields": ["name", "user_id"]},
            {"title": "Meta", "fields": ["state"]}
        ]
    }
}
```

---

## 🎨 Premium UI Design System

For a state-of-the-art feel, Znova uses a strict "Curved UI" philosophy:

- **Structural Containers (16px)**: Use `v.$radius-lg` for large frames like:
  - Base Form Sheets & Action Bars.
  - Sidebar Groups & Detached Pagers.
- **Interactive Elements (10px)**: Use `v.$radius-btn` for clickable items like:
  - Action Buttons (Main/Secondary).
  - Search Bars & Autocomplete Dropdowns.
  - Dialog buttons and form navigation.
- **Micro-interactions**: Subtle hover states, smooth transitions, and glassmorphism throughout the UI.

---

## 🧭 Menu Configuration

To keep core logic clean, menu structures are decoupled from the framework and reside in `backend/data/menus.py`.

- **Structure**: Uses `MenuItem` objects with `name`, `label`, `path`, `icon`, and optional `children`.
- **Nesting**: Supports infinite child nesting for complex navigation trees.
- **Permissions**: Menu visibility is role-aware (`groups` field).

---

## 🛠️ CLI Tools

- `python run.py`: Boots backend and frontend concurrently.
- `python setup_fresh.py`: Wipes DB and re-installs core data.
- `python setup_fresh.py --demo`: Re-installs everything including demo data for testing.
- `python test_loader.py`: (Internal) Validates data loading logic.
- `LOAD_DEMO_DATA=1`: Environment variable to enable demo records during setup.

---

## 🔍 Advanced Logic & Dynamics

### Search Configuration (`_search_config`)

You can define predefined filters and group_by options for list views using `_search_config`. This provides users with quick filtering and grouping capabilities.

```python
_search_config = {
    "filters": [
        {
            "name": "active_only",
            "label": "Active Only",
            "domain": "[('is_active', '=', True)]"
        },
        {
            "name": "my_records",
            "label": "My Records",
            "domain": "[('user_id', '=', user.id)]"  # Dynamic user context
        },
        {
            "name": "recent",
            "label": "Recent (Last 7 Days)",
            "domain": "[('created_at', '>=', datetime.now() - timedelta(days=7))]"
        }
    ],
    "group_by": [
        {
            "name": "by_status",
            "label": "By Status",
            "field": "status"
        },
        {
            "name": "by_user",
            "label": "By Assigned User",
            "field": "user_id"  # Works with many2one fields
        }
    ]
}
```

#### Filter Configuration

Each filter in the `filters` array supports:
- `name` (string, required): Unique identifier for the filter
- `label` (string, required): Display label in the UI
- `domain` (string, required): Domain expression as a string that will be evaluated

**Dynamic Filter Domains:**
Filters support dynamic expressions with access to:
- `user`: Current user recordset (e.g., `user.id`, `user.email`)
- `datetime`: Python datetime module
- `timedelta`: Python timedelta for date calculations
- `date`: Python date module
- Boolean values: `True`, `False`, `None`

**Example Filters:**
```python
"filters": [
    # Simple static filter
    {
        "name": "completed",
        "label": "Completed",
        "domain": "[('state', '=', 'done')]"
    },
    
    # User-specific filter
    {
        "name": "assigned_to_me",
        "label": "Assigned to Me",
        "domain": "[('assigned_user_id', '=', user.id)]"
    },
    
    # Date-based filter
    {
        "name": "this_month",
        "label": "This Month",
        "domain": "[('created_at', '>=', datetime.now().replace(day=1))]"
    },
    
    # Complex filter with multiple conditions
    {
        "name": "urgent_mine",
        "label": "My Urgent Tasks",
        "domain": "[('priority', '=', 'high'), ('user_id', '=', user.id), ('state', '!=', 'done')]"
    }
]
```

#### Group By Configuration

Each group_by option supports:
- `name` (string, required): Unique identifier for the grouping
- `label` (string, required): Display label in the UI
- `field` (string, required): Field name to group by

**Supported Field Types for Grouping:**
- Selection fields: Groups by each option value
- Many2one fields: Groups by related record (shows related record name)
- Char fields: Groups by exact value
- Boolean fields: Groups by True/False

**Example Group By:**
```python
"group_by": [
    # Group by selection field
    {
        "name": "by_status",
        "label": "By Status",
        "field": "state"
    },
    
    # Group by many2one field
    {
        "name": "by_team",
        "label": "By Team",
        "field": "team_id"
    },
    
    # Group by boolean field
    {
        "name": "by_active",
        "label": "By Active Status",
        "field": "is_active"
    }
]
```

### Relational Domains with Context

You can filter `Many2one` and `One2many` options using dynamic domains. These support **Global User Context**, allowing you to filter based on the currently logged-in user.

```python
# Generic domain (Literal values)
team_id = fields.Many2one("team", domain=[("state", "=", "active")])

# Contextual domain (using 'user' keywords)
venue_id = fields.Many2one("venue", domain=[("manager_id", "=", "user.id")])
# Supports: user.id, user.name, user.login, user.email
```

### Many2many Synchronization

When defining Many2many relationships, Znova automatically resolves intermediate table columns.

```python
# Definition
attendee_ids = fields.Many2many("res.partner", "event_partner_rel", "event_id", "partner_id")

# Interaction Syntax (Recordset Style)
match.write({
    "attendee_ids": [(6, 0, [partner_id1, partner_id2])] # Replace all
    # OR
    "attendee_ids": [partner_id1, partner_id2] # Shortcut syntax supported by Znova
})
```

---

## 🎭 Advanced UI Architecture

### The "Floating Sheet" Pattern

To provide a premium feel, the main content area is designed as a floating block over a fixed background.

1.  **Fixed Navigation**: The Sidebar (`MainLayout.vue`) and Top Breadcrumbs are fixed.
2.  **Floating Action Bar**: Action buttons are grouped in a floating bar at the top of the view.
3.  **Sheet Container**: The actual form/list content is inside a `.form-sheet-expanded` or `.table-view` container with `v.$radius-lg` and `v.$shadow-lg`.
4.  **Integrated Pager**: The pagination footer in List view is a standalone floating block, distinct from the table sheet.

### Skeleton Development & Testing

Skeletons must perfectly match the final layout to avoid "jumping" content:

- **Bare Skeletons**: `TableSkeleton.vue` and `FormSkeleton.vue` are "bare" (no borders/shadows). They are wrapped by the parent view's real CSS classes.
- **Verification Pattern**: During development, use a `sleep(1000)` helper in the composables (`useForm.ts`, `useList.ts`) to hold the loading state and verify skeleton alignment.

```typescript
// Pattern for testing skeletons in composables
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export function useForm(modelName: string) {
    // ...
    const fetchRecord = async (id: number) => {
        loading.value = true;
        const res = await api.get(...);
        await sleep(1000); // Artificial delay for testing UI
        loading.value = false;
    };
}
```

---

## 🧙‍♂️ TransientModel (Wizards)

For temporary records like popups, confirmation dialogs, or multi-step wizards, use `TransientModel`.

### Key Features

- **Database Backed**: Records are stored in the DB but auto-cleaned regularly.
- **Auto-Cleanup**: A system cron job deletes old transient records.
- **Simplified API**: Supports easy `create` -> `execute` flow.

### Definition Example

```python
from backend.core.transient_model import TransientModel

class LaunchMissionWizard(TransientModel):
    __tablename__ = "mission_launch_wizard"
    _model_name_ = "mission.launch.wizard"
    _description_ = "Confirm Mission Launch"

    mission_id = fields.Many2one("mission", release=True)
    confirm_code = fields.Char(label="Confirmation Code")

    def action_launch(self):
        if self.confirm_code != "GO":
             raise UserError("Invalid code!")

        self.mission_id.write({'state': 'launched'})

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"message": "Liftoff!", "type": "success", "refresh": True}
        }
```

### Triggering a Wizard

Return an action with `target: 'new'`:

```python
def action_open_launch_wizard(self):
    return {
        "type": "ir.actions.act_window",
        "res_model": "mission.launch.wizard",
        "target": "new",
        "context": {"default_mission_id": self.id},
        "name": "Launch Mission"
    }
```


---

## 🎨 Dialog System

Znova provides three types of reusable dialog components for user interactions: Alert, Confirm, and Prompt dialogs.

### Available Dialog Types

1. **AlertDialog** - Simple notification with OK button
2. **ConfirmDialog** - Yes/No confirmation with customizable severity
3. **PromptDialog** - Input dialog for collecting user data

### Usage with `useDialog` Composable

The `useDialog` composable provides a simple API for showing dialogs from anywhere in your application.

```typescript
import { useDialog } from '@/composables/useDialog';

const { alert, confirm, prompt } = useDialog();
```

### Alert Dialog

Show informational messages, success notifications, warnings, or errors.

```typescript
// Basic alert
await alert({
  message: 'Operation completed successfully!'
});

// Success alert
await alert({
  title: 'Success',
  message: 'Your changes have been saved.',
  type: 'success'
});

// Warning alert
await alert({
  title: 'Warning',
  message: 'This action cannot be undone.',
  type: 'warning'
});

// Error alert
await alert({
  title: 'Error',
  message: 'Failed to save changes. Please try again.',
  type: 'error',
  confirmText: 'Got it'
});
```

**Alert Options:**
- `title` (string, optional): Dialog title (default: 'Alert')
- `message` (string, required): Message to display
- `type` ('info' | 'success' | 'warning' | 'error', optional): Alert type (default: 'info')
- `confirmText` (string, optional): OK button text (default: 'OK')

### Confirm Dialog

Request user confirmation before performing actions.

```typescript
// Basic confirmation
const confirmed = await confirm({
  message: 'Are you sure you want to proceed?'
});

if (confirmed) {
  // User clicked "Confirm"
  performAction();
}

// Danger confirmation (red button)
const deleteConfirmed = await confirm({
  title: 'Delete Item',
  message: 'Are you sure you want to delete this item? This action cannot be undone.',
  severity: 'danger',
  confirmText: 'Yes, Delete',
  cancelText: 'No, Keep It'
});

// Warning confirmation
const cancelConfirmed = await confirm({
  title: 'Cancel Match',
  message: 'Are you sure you want to cancel this match? All progress will be lost.',
  severity: 'warning',
  confirmText: 'Yes, Cancel Match',
  cancelText: 'No, Continue'
});
```

**Confirm Options:**
- `title` (string, optional): Dialog title (default: 'Confirm')
- `message` (string, required): Confirmation message
- `severity` ('info' | 'warning' | 'danger', optional): Button color (default: 'info')
- `confirmText` (string, optional): Confirm button text (default: 'Confirm')
- `cancelText` (string, optional): Cancel button text (default: 'Cancel')

**Returns:** `Promise<boolean>` - true if confirmed, false if cancelled

### Prompt Dialog

Collect user input through a dialog.

```typescript
// Basic text input
const name = await prompt({
  title: 'Enter Name',
  message: 'Please enter your name:',
  placeholder: 'John Doe'
});

if (name) {
  console.log('User entered:', name);
} else {
  console.log('User cancelled');
}

// Number input
const score = await prompt({
  title: 'Enter Score',
  message: 'Enter the final score:',
  inputType: 'number',
  defaultValue: '0',
  placeholder: 'Enter score...'
});

// Email input
const email = await prompt({
  title: 'Email Address',
  message: 'Please provide your email:',
  inputType: 'email',
  placeholder: 'user@example.com',
  required: true
});

// Optional input (not required)
const notes = await prompt({
  title: 'Additional Notes',
  message: 'Add any notes (optional):',
  required: false,
  placeholder: 'Enter notes...'
});
```

**Prompt Options:**
- `title` (string, optional): Dialog title (default: 'Input')
- `message` (string, optional): Instruction message
- `placeholder` (string, optional): Input placeholder (default: 'Enter value...')
- `defaultValue` (string, optional): Pre-filled value (default: '')
- `inputType` ('text' | 'number' | 'email' | 'password', optional): Input type (default: 'text')
- `required` (boolean, optional): Whether input is required (default: true)
- `confirmText` (string, optional): OK button text (default: 'OK')
- `cancelText` (string, optional): Cancel button text (default: 'Cancel')

**Returns:** `Promise<string | null>` - input value if confirmed, null if cancelled

### Using Dialogs in Button Actions

You can intercept button actions in BaseForm to show confirmation dialogs:

```typescript
// In BaseForm.vue or similar component
const onBtnAction = async (btn: any) => {
    // Show confirmation for dangerous actions
    if (btn.name === 'cancel_match') {
        const { confirm } = await import('../../composables/useDialog');
        const confirmed = await confirm({
            title: 'Cancel Match',
            message: 'Are you sure you want to cancel this match?',
            severity: 'warning',
            confirmText: 'Yes, Cancel',
            cancelText: 'No, Keep'
        });
        
        if (!confirmed) {
            return; // User cancelled
        }
    }
    
    // Proceed with action
    emit('action', btn);
};
```

### Backend Integration

Define actions in your model that work with frontend dialogs:

#### Method 1: Frontend-Only (Intercept in BaseForm)

```python
class Match(ZnovaModel):
    # ... model definition ...
    
    _ui_views = {
        "form": {
            "header_buttons": [
                {
                    "name": "cancel_match",
                    "label": "Cancel Match",
                    "type": "secondary",
                    "method": "action_cancel_match"
                }
            ]
        }
    }
    
    def action_cancel_match(self):
        """Cancel the match - frontend intercepts and shows dialog."""
        self.write({'match_status': 'draft'})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {"message": "Match cancelled", "type": "warning"}
        }
```

#### Method 2: Backend-Driven Dialogs (Recommended)

Return dialog actions directly from Python:

```python
def action_cancel_match(self):
    """Return a confirmation dialog action."""
    return {
        "type": "ir.actions.dialog",
        "dialog_type": "confirm",
        "title": "Cancel Match",
        "message": f"Are you sure you want to cancel '{self.name}'?",
        "severity": "warning",
        "confirmText": "Yes, Cancel",
        "cancelText": "No, Keep",
        "on_confirm": {
            "method": "action_do_cancel_match",
            "params": {}
        }
    }

def action_do_cancel_match(self):
    """Actually cancel after confirmation."""
    self.write({'match_status': 'draft'})
    return {
        "type": "ir.actions.client",
        "tag": "display_notification",
        "params": {"message": "Match cancelled", "refresh": True}
    }
```

### Backend Dialog Actions

You can return dialog actions from any model method:

#### Alert Dialog from Backend

```python
def action_show_info(self):
    return {
        "type": "ir.actions.dialog",
        "dialog_type": "alert",
        "title": "Information",
        "message": "This is an informational message.",
        "alert_type": "info",  # info, success, warning, error
        "confirmText": "Got it"
    }
```

#### Confirm Dialog from Backend

```python
def action_delete_with_confirm(self):
    return {
        "type": "ir.actions.dialog",
        "dialog_type": "confirm",
        "title": "Delete Item",
        "message": "This action cannot be undone. Continue?",
        "severity": "danger",  # info, warning, danger
        "confirmText": "Yes, Delete",
        "cancelText": "Cancel",
        "on_confirm": {
            "method": "action_do_delete",
            "params": {}
        },
        "on_cancel": {
            "method": "action_cancel_delete",
            "params": {}
        }
    }
```

#### Prompt Dialog from Backend

```python
def action_rename_item(self):
    return {
        "type": "ir.actions.dialog",
        "dialog_type": "prompt",
        "title": "Rename Item",
        "message": "Enter new name:",
        "placeholder": "New name...",
        "defaultValue": self.name,
        "inputType": "text",  # text, number, email, password
        "required": True,
        "confirmText": "Rename",
        "cancelText": "Cancel",
        "on_confirm": {
            "method": "action_do_rename",
            "params": {}  # 'value' will be added automatically
        }
    }

def action_do_rename(self, value):
    """Rename with the provided value."""
    self.write({'name': value})
    return {
        "type": "ir.actions.client",
        "tag": "display_notification",
        "params": {"message": f"Renamed to '{value}'", "refresh": True}
    }
```

### Dialog Action Structure

```python
{
    "type": "ir.actions.dialog",
    "dialog_type": "alert" | "confirm" | "prompt",
    
    # Common fields
    "title": "Dialog Title",
    "message": "Dialog message",
    
    # Alert-specific
    "alert_type": "info" | "success" | "warning" | "error",
    
    # Confirm-specific
    "severity": "info" | "warning" | "danger",
    
    # Prompt-specific
    "placeholder": "Enter value...",
    "defaultValue": "default",
    "inputType": "text" | "number" | "email" | "password",
    "required": True | False,
    
    # Button text
    "confirmText": "OK",
    "cancelText": "Cancel",
    
    # Callbacks
    "on_confirm": {
        "method": "method_name",  # Method to call on confirm
        "params": {}              # Additional params
    },
    "on_cancel": {
        "method": "method_name",  # Method to call on cancel
        "params": {}
    }
}
```

### Dialog Components

The dialog components are globally available in `App.vue`:

```vue
<template>
  <router-view />
  
  <!-- Global Dialog Components -->
  <AlertDialog ... />
  <ConfirmDialog ... />
  <PromptDialog ... />
</template>
```

### Best Practices

1. **Use appropriate severity**: 
   - `info` for general confirmations
   - `warning` for actions that can be undone
   - `danger` for destructive actions (delete, cancel, etc.)

2. **Clear messaging**: Write concise, actionable messages that explain what will happen

3. **Descriptive button text**: Use action-oriented text like "Yes, Delete" instead of just "OK"

4. **Handle cancellation**: Always check the return value and handle the case where user cancels

5. **Async/await**: Dialogs return promises, so use async/await for clean code

### Example: Complete Workflow

```typescript
// In a Vue component
import { useDialog } from '@/composables/useDialog';

const { alert, confirm, prompt } = useDialog();

async function deleteMatch(matchId: number) {
  // Step 1: Confirm deletion
  const confirmed = await confirm({
    title: 'Delete Match',
    message: 'Are you sure you want to delete this match? This action cannot be undone.',
    severity: 'danger',
    confirmText: 'Yes, Delete',
    cancelText: 'Cancel'
  });
  
  if (!confirmed) return;
  
  // Step 2: Perform deletion
  try {
    await api.delete(`/models/bcm.match/${matchId}`);
    
    // Step 3: Show success
    await alert({
      title: 'Success',
      message: 'Match has been deleted successfully.',
      type: 'success'
    });
    
    // Refresh list or navigate away
    router.push('/models/bcm.match');
  } catch (error) {
    // Step 4: Show error
    await alert({
      title: 'Error',
      message: 'Failed to delete match. Please try again.',
      type: 'error'
    });
  }
}
```

---


## 📋 Audit Log System

Znova includes a comprehensive audit log system that tracks field changes across all models. It records who changed what field, when, and from what value to what value.

### Features

- **Field-level tracking**: Track specific fields by adding `tracking=True` to field metadata
- **Automatic tracking**: Changes are automatically captured on write/create operations
- **User attribution**: Records which user made each change
- **Timeline view**: Beautiful sidebar showing change history with timeline
- **Dark/Light theme support**: Fully styled for both themes
- **Export functionality**: Export audit logs as JSON

### Enabling Audit Tracking

#### Step 1: Add `tracking=True` to Fields

To enable tracking on a field, add `tracking=True` to the field definition:

```python
from backend.core.znova_model import ZnovaModel
from backend.core import fields

class Match(ZnovaModel):
    __tablename__ = "bcm_match"
    _model_name_ = "bcm.match"
    
    # Tracked fields
    name = fields.Char(label="Match Name", required=True, tracking=True)
    team_a_id = fields.Many2one("bcm.team", label="Team A", tracking=True)
    team_b_id = fields.Many2one("bcm.team", label="Team B", tracking=True)
    match_status = fields.Selection([
        ('draft', 'Scheduled'),
        ('live', 'Match in Progress'),
        ('completed', 'Finished')
    ], label="Status", default='draft', tracking=True)
    
    # Not tracked
    notes = fields.Text(label="Notes")  # No tracking parameter
```

**Supported Field Types for Tracking:**
- `Char`, `Text`, `Integer`, `Boolean`
- `Date`, `DateTime`
- `Selection`
- `Many2one` (shows related record name)
- `One2many`, `Many2many` (shows record count)

#### Step 2: Enable Audit Log in Form View

Add `show_audit_log: True` to the form view definition:

```python
_ui_views = {
    "list": {
        "fields": ["name", "team_a_id", "team_b_id", "match_status"]
    },
    "form": {
        "show_audit_log": True,  # Enable audit log sidebar
        "groups": [
            {
                "title": "Match Details",
                "fields": ["name", "team_a_id", "team_b_id"]
            }
        ]
    }
}
```

### How It Works

#### Backend Tracking

1. **On Record Creation**: A "Record Created" entry is added to the audit log
2. **On Field Change**: When a tracked field is modified via `write()`:
   - Old value is captured before the change
   - New value is captured after the change
   - An audit log entry is created with both values
3. **User Attribution**: The current user ID is automatically captured from the request context

#### Audit Log Model

The audit log entries are stored in the `audit.log` model with these fields:

```python
class AuditLog(ZnovaModel):
    __tablename__ = "audit_log"
    _model_name_ = "audit.log"
    
    res_model = fields.Char(label="Model Name")      # e.g., "bcm.match"
    res_id = fields.Integer(label="Record ID")        # e.g., 42
    field_name = fields.Char(label="Field Name")      # e.g., "match_status"
    field_label = fields.Char(label="Field Label")    # e.g., "Status"
    old_value = fields.Text(label="Old Value")        # e.g., "Draft"
    new_value = fields.Text(label="New Value")        # e.g., "Live"
    user_id = fields.Many2one("user", label="Changed By")
    changed_at = fields.DateTime(label="Changed At")
    change_type = fields.Selection([
        ('create', 'Created'),
        ('write', 'Updated'),
        ('delete', 'Deleted')
    ], label="Change Type")
```

### Frontend Display

When `show_audit_log: True` is set, a sidebar appears on the right side of the form view showing:

- **Timeline view**: Vertical timeline with dots indicating change type
- **Change details**: Field name, old/new values, user who made the change
- **Relative timestamps**: "2m ago", "1h ago", "1d ago"
- **User avatars**: Initials of the user who made the change
- **Export button**: Download audit log as JSON

#### Audit Log Sidebar Features

```vue
<!-- Automatically shown when show_audit_log: true -->
<AuditLogSidebar
  :modelName="modelName"
  :recordId="formData.id"
  :visible="true"
/>
```

**Sidebar displays:**
- Latest changes at the top
- Color-coded dots (blue for latest, gray for older)
- Old → New value comparison
- User information with avatar
- Relative time display
- Export functionality

### API Endpoint

**GET** `/api/v1/model/{model_name}/{id}/audit-logs`

Returns audit log entries for a specific record, ordered by most recent first.

**Example Request:**
```bash
GET /api/v1/model/bcm.match/42/audit-logs
```

**Example Response:**
```json
[
  {
    "id": 123,
    "field_name": "match_status",
    "field_label": "Status",
    "old_value": "Draft",
    "new_value": "Live",
    "change_type": "write",
    "changed_at": "2024-02-15T10:30:00",
    "user": {
      "id": 1,
      "name": "Admin User",
      "email": "admin@example.com"
    }
  },
  {
    "id": 122,
    "field_name": "__record__",
    "field_label": "Record",
    "old_value": "",
    "new_value": "Created",
    "change_type": "create",
    "changed_at": "2024-02-15T10:00:00",
    "user": {
      "id": 1,
      "name": "Admin User",
      "email": "admin@example.com"
    }
  }
]
```

### Value Formatting

The audit log system automatically formats values for display:

- **Many2one**: Shows related record name (e.g., "Team Alpha")
- **Many2many**: Shows comma-separated list of record names (e.g., "Player A, Player B, Player C")
- **Selection**: Shows label (e.g., "Live" instead of "live")
- **Boolean**: Shows "Yes" or "No"
- **Date/DateTime**: Formatted as readable date strings
- **One2many**: Shows record count (e.g., "3 record(s)")

#### Smart Change Detection

The audit log system uses intelligent comparison to avoid false positives:

**Many2one fields**: Compares IDs, not display names
- Old: Team object with ID 1 → "Royal Challengers India"
- New: ID 1 → "Royal Challengers India"
- Result: No audit log (IDs are the same)

**Many2many fields**: Compares sets of IDs, displays names
- Old: [Record(1), Record(2), Record(3)]
- New: [1, 2, 3]
- Result: No audit log (ID sets are the same)
- Display: "Player A, Player B, Player C" (not just "3 record(s)")

**DateTime fields**: Normalizes format before comparison
- Old: "2026-02-14 20:00:00"
- New: "2026-02-14T20:00:00"
- Result: No audit log (same datetime, different format)

This ensures audit logs only show actual changes, not formatting differences.

### Example: Complete Implementation

```python
from backend.core.znova_model import ZnovaModel
from backend.core import fields

class Session(ZnovaModel):
    __tablename__ = "bcm_session"
    _model_name_ = "bcm.session"
    _name_field_ = "name"
    
    # Tracked fields
    name = fields.Char(label="Session Name", required=True, tracking=True)
    venue_id = fields.Many2one("bcm.venue", label="Venue", tracking=True)
    start_datetime = fields.DateTime(label="Start Time", tracking=True)
    end_datetime = fields.DateTime(label="End Time", tracking=True)
    total_cost = fields.Integer(label="Total Cost", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Live'),
        ('done', 'Completed')
    ], label="Status", default="draft", tracking=True)
    
    # Not tracked
    notes = fields.Text(label="Notes")  # Internal notes, no tracking needed
    
    _ui_views = {
        "list": {
            "fields": ["name", "venue_id", "start_datetime", "state"]
        },
        "form": {
            "show_audit_log": True,  # Enable audit log sidebar
            "groups": [
                {
                    "title": "Session Details",
                    "fields": ["name", "venue_id", "start_datetime", "end_datetime"]
                },
                {
                    "title": "Status & Cost",
                    "fields": ["state", "total_cost", "notes"]
                }
            ]
        }
    }
```

### When to Use Audit Tracking

**Good Use Cases:**
- Critical business fields (status, amounts, dates)
- Compliance requirements (who approved what)
- Important relationships (assigned user, team, etc.)
- Configuration changes (settings, thresholds)

**Avoid Tracking:**
- Computed fields (they change automatically)
- Internal system fields (created_at, updated_at)
- Large text fields that change frequently (notes, descriptions)
- Fields that change on every save (timestamps, counters)

### Performance Considerations

- Audit logs are created in the same transaction as the main operation
- Failed audit log creation does not break the main operation (logged as error)
- Indexes are created on `res_model`, `res_id`, `user_id`, and `changed_at` for fast queries
- Only tracked fields are monitored (not all fields)
- Audit logs are automatically refreshed after save operations

### Customization

#### Custom Value Formatting

You can customize how values are formatted in the audit log by modifying `backend/core/audit_tracker.py`:

```python
def format_value_for_audit(value: Any, field_type: str, field_meta: Dict = None) -> str:
    """Format a field value for storage in audit log."""
    if value is None:
        return ""
    
    # Add custom formatting logic here
    if field_type == "my_custom_type":
        return f"Custom: {value}"
    
    # Default formatting...
    return str(value)
```

#### Filtering Audit Logs

You can filter audit logs in the frontend by modifying the API call:

```typescript
// In AuditLogSidebar.vue
const fetchLogs = async () => {
  const response = await api.get(
    `/api/v1/model/${props.modelName}/${props.recordId}/audit-logs`,
    {
      params: {
        field_name: 'match_status',  // Filter by specific field
        user_id: 1,                   // Filter by user
        from_date: '2024-01-01'       // Filter by date range
      }
    }
  );
  logs.value = response.data;
};
```

### Troubleshooting

**Audit log not showing:**
1. Check that `show_audit_log: True` is set in `_ui_views.form`
2. Verify the record has an ID (audit log doesn't show for new records)
3. Check browser console for API errors

**Changes not being tracked:**
1. Verify `tracking=True` is set on the field
2. Check that the field is actually changing (old value ≠ new value)
3. Ensure user_id is being passed to write() method
4. Check backend logs for audit tracker errors

**Performance issues:**
1. Reduce the number of tracked fields
2. Add database indexes if querying audit logs frequently
3. Consider implementing audit log archiving for old records

---
