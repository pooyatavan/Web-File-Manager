$.ajax({
  type: "GET",
  url: "/get_options",
  contentType: "application/json",
  dataType: "json",
  success: function(response) {
    pers = response[0];  // Permissions data
    users = response[1];  // User data

    // Create the select dropdown for users
    const selectElement = document.createElement('select');
    selectElement.setAttribute('id', 'permission_select');
    selectElement.className = 'form-select';

    users.forEach(user => {
      const optionElement = document.createElement('option');
      optionElement.value = user[0]; // User ID
      optionElement.text = user[1];  // User Name
      selectElement.appendChild(optionElement);
    });

    // Create a container for checkboxes
    const checkboxGroup = document.createElement('div');
    checkboxGroup.className = 'checkbox-group';

    // Map to store each user's checkbox group by user ID
    const checkboxesMap = {};

    // Generate checkboxes for each permission
    pers.forEach((userPermissions) => {
      const userId = userPermissions.id;
      const userCheckboxGroup = document.createElement('div');
      userCheckboxGroup.className = 'user-checkbox-group';
      userCheckboxGroup.setAttribute('data-user-id', userId);  // Store userId as a data attribute

      // Initially hide all user checkboxes
      userCheckboxGroup.style.display = 'none';

      Object.entries(userPermissions).forEach(([key, value]) => {
        if (key !== 'id') {  // Skip the 'id' field since it's not a permission
          const label = document.createElement('label');
          label.className = 'checkbox-container';
         
          const checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.name = key;
          checkbox.value = '1';
          checkbox.checked = value === 1;  // Set checkbox based on permission value
          
          const span = document.createElement('span');
          span.className = 'checkbox-label';
          span.textContent = key;
         
          label.appendChild(checkbox);
          label.appendChild(span);
          userCheckboxGroup.appendChild(label);
        }
      });

      checkboxGroup.appendChild(userCheckboxGroup); // Add each user's checkboxes to the group

      // Store the group of checkboxes in the map
      checkboxesMap[userId] = userCheckboxGroup;
    });

    // Append the select and checkbox group to the form
    const form = document.getElementById('permission_form');
    form.appendChild(selectElement);
    form.appendChild(checkboxGroup);

    // Set up event listener for the select element
    selectElement.addEventListener('change', (event) => {
      const selectedUserId = event.target.value;

      // Hide/show checkboxes based on the selected user
      Object.keys(checkboxesMap).forEach(userId => {
        const userCheckboxGroup = checkboxesMap[userId];
        if (userId === selectedUserId) {
          userCheckboxGroup.style.display = 'flex'; // Show this user's checkboxes
        } else {
          userCheckboxGroup.style.display = 'none'; // Hide all other users' checkboxes
        }
      });
    });

    // Optionally, trigger a change event to display the checkboxes for the first user initially
    selectElement.dispatchEvent(new Event('change'));

    // Add a submit button to send data
    const submitButton = document.createElement('button');
    submitButton.textContent = 'تایید';
    submitButton.classList.add('btn')
    submitButton.setAttribute('type', 'button');  // prevent form submit behavior
    submitButton.addEventListener('click', function() {
      submitPermissions();
    });
    form.appendChild(submitButton);
  }
});

// Function to collect the selected checkbox values and send them to Flask
function submitPermissions() {
  const selectedUserId = document.getElementById('permission_select').value;

  // Get all checkboxes (checked and unchecked) for the selected user
  const selectedPermissions = {};
  const checkboxes = document.querySelectorAll(`.user-checkbox-group[data-user-id="${selectedUserId}"] input[type="checkbox"]`);

  checkboxes.forEach(checkbox => {
    // Set permission to '1' if checked, '0' if not
    selectedPermissions[checkbox.name] = checkbox.checked ? '1' : '0';
  });

  // Prepare data to be sent to Flask
  const data = {
    user_id: selectedUserId,  // Send the selected user ID
    permissions: selectedPermissions // Send selected permissions
  };

  // Send data to Flask using an AJAX POST request
  $.ajax({
    type: "POST",
    url: "/update_permissions",  // Flask endpoint
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify(data),  // Send the data as JSON
    success: function(response) {
      alert('ُسطح دسترسی اعمال شد.');
    },
    error: function(xhr, status, error) {
      alert('ُسطح دسترسی اعمال شد.');
    }
  });
}
