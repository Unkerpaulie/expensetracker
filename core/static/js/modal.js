  function createEditModal(editBtnId) {
    const editModal = document.getElementById("editModal");
    const expData = document.getElementById("editBtn" + editBtnId);

    editModal.innterHTML = `
    <div class="card mt-5" data-bs-theme="auto">
      <div class="card-header"></div>
      <div class="card-body">
        <h4 class="card-title p-2">Expense details</h4>
          <form action="" method="post">
              {% csrf_token %}

              <div class="form-group mt-3">
                  <label class="form-label" for="category">Category</label>
                  <div class="input-group">
                      <select class="form-select" name="category">
                          {% for category in categories %}
                          <option value="{{ category.name }}"{% if form_data.category == category.name %} selected{% endif %}>{{ category.name }}</option>
                          {% endfor %}
                      </select>
                      <button class="btn btn-outline-primary" type="button" data-bs-toggle="modal" data-bs-target="#addCategoryModal">Add Category</button>
                  </div>
              </div>

              <div class="form-group mt-3">
                  <label class="form-label" for="description">Description</label>
                  <input type="text" name="description" class="form-control form-control-sm" value="{{ form_data.description }}">
              </div>
              
              <div class="form-group mt-3">
                  <label class="form-label" for="amount">Amount</label>
                  <input type="number" name="amount" class="form-control" value="{{ form_data.amount }}" step="0.01" />
              </div>
               
              <div class="form-group mt-3">
                  <label class="form-label" for="date">Expense Date</label>
                  <input type="date" name="expense_date" class="form-control form-control-sm" value="{{ form_data.expense_date }}">
              </div>
              
              <div class="d-grid gap-2">
                  <button type="submit" id="submit" class="btn btn-primary mt-3">Submit</button>
              </div>
          </form>
      </div>
  </div>

    `;
  }

