function disableRightClick(event) {
    if (event.button == 2) {
      event.preventDefault();
      alert("اجازه راست کلیک ندارید");
      return false;
    }
  }