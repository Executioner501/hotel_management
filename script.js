function fetchChefs() {
    fetch('/get-chefs')
        .then(response => response.json())
        .then(data => {
            let output = "<table border='1'><tr><th>SSN</th><th>Name</th><th>Join Date</th><th>Specialty Cuisine</th></tr>";
            data.forEach(chef => {
                output += `<tr>
                    <td>${chef.ssn}</td>
                    <td>${chef.name}</td>
                    <td>${chef.join_date}</td>
                    <td>${chef.specialty_cuisine}</td>
                </tr>`;
            });
            output += "</table>";
            document.getElementById("chef-list").innerHTML = output;
        })
        .catch(error => console.error('Error:', error));
}

function getBranch() {
    fetch('/get-branches')
        .then(response => response.json())
        .then(data => {
            let output = "<table border='1'><tr><th>Branch ID</th><th>Name</th><th>City</th><th>State</th><th>Start Date</th><th>Planned Revenue</th><th>Planned Expenditure</th></tr>";
            data.forEach(branch => {
                output += `<tr>
                    <td>${branch.branch_id}</td>
                    <td>${branch.name}</td>
                    <td>${branch.city}</td>
                    <td>${branch.state}</td>
                    <td>${branch.start_date}</td>
                    <td>${branch.planned_revenue || 'N/A'}</td>
                    <td>${branch.planned_expenditure || 'N/A'}</td>
                </tr>`;
            });
            output += "</table>";
            document.getElementById("branch-list").innerHTML = output;
        })
        .catch(error => console.error('Error:', error));
}
$(document).ready(function() {
    // View chefs based on selected branch
    $('#view-chefs-btn').click(function() {
        let branchId = $('#branch-dropdown').val();
        $.get("/get-chefs?branch_id=" + branchId, function(data) {
            let chefTableBody = $('#chef-table tbody');
            chefTableBody.empty();
            data.forEach(function(chef) {
                chefTableBody.append(
                    `<tr>
                        <td>${chef.ssn}</td>
                        <td>${chef.name}</td>
                        <td>${chef.join_date}</td>
                        <td>${chef.specialty_cuisine}</td>
                    </tr>`
                );
            });
        });
    });

    // Save or update chef
    $('#chef-form').submit(function(e) {
        e.preventDefault();
        let chefData = $(this).serialize();
        $.ajax({
            url: "/save-chef",
            type: "POST",
            data: chefData,
            success: function(response) {
                alert(response.message);
                $('#view-chefs-btn').click(); // Refresh chef list
            },
            error: function(error) {
                alert(error.responseJSON.error);
            }
        });
    });
});