# AutoMarket Manual Testing Checklist

## Pre-Test Setup
- [ ] Server is running on http://localhost:5000
- [ ] Admin credentials available (admin/admin123)
- [ ] Database is accessible and initialized

## Test Case 1: Admin Login
**Objective**: Verify admin can log into the system
- [ ] Navigate to `/admin/login`
- [ ] Enter username: `admin`
- [ ] Enter password: `admin123`
- [ ] Click Login button
- [ ] **Expected**: Redirected to admin dashboard

## Test Case 2: Add Vehicle Form - UI Elements
**Objective**: Verify all form elements are visible and functional
- [ ] Click "Add New Vehicle" button
- [ ] **Expected**: Modal opens with wizard interface
- [ ] **Expected**: Progress indicators show 6 steps
- [ ] **Expected**: Step 1 is highlighted
- [ ] **Expected**: Form fields have dark, visible text
- [ ] **Expected**: Placeholders are visible

## Test Case 3: Wizard Navigation
**Objective**: Test step-by-step navigation
- [ ] Verify "Next Step" button is visible
- [ ] Click "Next Step" to go to Step 2 (Engine)
- [ ] **Expected**: Progress indicator updates
- [ ] **Expected**: "Previous Step" button appears
- [ ] Navigate through all 6 steps
- [ ] **Expected**: Last step shows "Save Vehicle" button

## Test Case 4: Form Validation
**Objective**: Test required field validation
- [ ] Try to click "Next Step" without filling required fields
- [ ] **Expected**: Validation message appears
- [ ] **Expected**: Missing fields are highlighted in red
- [ ] Fill required fields and try again
- [ ] **Expected**: Can proceed to next step

## Test Case 5: Complete Vehicle Entry
**Objective**: Add a complete vehicle record

### Step 1: Basic Information
- [ ] Title: `2023 Tesla Model 3 Performance - Test Vehicle`
- [ ] Category: `Cars`
- [ ] Make: `Tesla`
- [ ] Model: `Model 3`
- [ ] Year: `2023`
- [ ] Price: `52000`
- [ ] Mileage: `12500`
- [ ] Description: `Test vehicle for automation testing`

### Step 2: Engine Information
- [ ] Fuel Type: `Electric`
- [ ] Transmission: `Automatic`
- [ ] Engine Size: `Electric Motor` (optional)
- [ ] Horsepower: `450` (optional)

### Step 3: Ownership & History
- [ ] Number of Owners: `1` (optional)
- [ ] Odometer: `12500` (optional)

### Step 4: Insurance & Documentation
- [ ] VIN Number: `5YJ3E1EA1NF123456` (optional)

### Step 5: Features & Condition
- [ ] Exterior Color: `Pearl White` (optional)
- [ ] Interior Color: `Black` (optional)
- [ ] Features: `Autopilot, Premium Audio, Glass Roof` (optional)

### Step 6: Contact & Images
- [ ] Contact Name: `Test User`
- [ ] Contact Phone: `(555) 123-4567`
- [ ] Images: Upload at least one test image (optional)

### Final Submission
- [ ] Click "Save Vehicle" button
- [ ] **Expected**: Success message appears
- [ ] **Expected**: Modal closes
- [ ] **Expected**: Page refreshes or updates

## Test Case 6: Verify Vehicle Added
**Objective**: Confirm vehicle appears in the list
- [ ] Check vehicles table on dashboard
- [ ] **Expected**: Tesla Model 3 appears in the list
- [ ] **Expected**: All details are correctly displayed
- [ ] **Expected**: Status is "Available"

## Test Case 7: Edit Vehicle
**Objective**: Test editing functionality
- [ ] Click "Edit" button on the test vehicle
- [ ] **Expected**: Modal opens with pre-filled data
- [ ] **Expected**: Title shows "Edit Vehicle"
- [ ] Modify the price to `51000`
- [ ] Save changes
- [ ] **Expected**: Updated price is displayed

## Test Case 8: Vehicle Status Toggle
**Objective**: Test status change functionality
- [ ] Click status toggle button on test vehicle
- [ ] **Expected**: Confirmation dialog appears
- [ ] Confirm the change
- [ ] **Expected**: Status updates to "Sold"
- [ ] **Expected**: Statistics update accordingly

## Test Case 9: Delete Vehicle
**Objective**: Test deletion functionality
- [ ] Click "Delete" button on test vehicle
- [ ] **Expected**: Confirmation dialog appears
- [ ] Confirm deletion
- [ ] **Expected**: Vehicle removed from list
- [ ] **Expected**: Statistics update accordingly

## Browser Compatibility Tests
Test the above scenarios in:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Edge

## Mobile Responsiveness Tests
- [ ] Open on mobile device or resize browser window
- [ ] **Expected**: Form remains usable
- [ ] **Expected**: Wizard navigation works on mobile
- [ ] **Expected**: All text remains visible

## Performance Tests
- [ ] Time to load admin dashboard: _____ seconds
- [ ] Time to open add vehicle modal: _____ seconds
- [ ] Time to submit form: _____ seconds
- [ ] **Expected**: All actions complete within 3 seconds

## Accessibility Tests
- [ ] Tab through form using keyboard only
- [ ] **Expected**: All elements are reachable
- [ ] **Expected**: Focus indicators are visible
- [ ] Test with screen reader (if available)

## Edge Cases
- [ ] Try to enter extremely long text in fields
- [ ] Try to enter special characters
- [ ] Try to upload very large images
- [ ] Try to submit with network disconnected

## Test Results Summary
- **Total Test Cases**: 9
- **Passed**: _____
- **Failed**: _____
- **Blocked**: _____
- **Success Rate**: _____%

## Notes
- Document any bugs or issues found
- Include screenshots for visual issues
- Note browser/device specific problems
- Record performance metrics