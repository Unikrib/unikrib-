const Confirm = {
    open(options) {
      options = Object.assign({}, {
        title: "",
        message: "",
        okText: "OK",
        cancelText: "Cancel",
        onok: function() {},
        oncancel: function() {}

      }, options);

      const html = `
         <div class="confirm">
            <div class="confirm--window">
               <div class="confirm--titlebar">
                   <h3 class="confirm--title">${options.title}</h3>
                   <button class="confirm--close">&times;</button>
               </div>
               <div class="confirm--content">
                   ${options.message}
               </div>
               <div class="confirm--buttons">
                  <button class="confirm--button confirm--button--ok delete--button-fill">${options.okText}</button>
                  <button class="confirm--button confirm--button--cancel cancel--button-fill">${options.cancelText}</button>
               </div>
           </div>
         </div>
      `;

      const template = document.createElement("template");
      template.innerHTML = html;

      const confirmEl = template.content.querySelector(".confirm");
      const btnClose = template.content.querySelector(".confirm--close");
      const btnDelete = template.content.querySelector(".confirm--button--ok");
      const btnCancel = template.content.querySelector(".confirm--button--cancel");

      confirmEl.addEventListener("click", e => {
        if (e.target === confirmEl) {
          options.oncancel();
          this._close(confirmEl)
        }
      }); 

      btnDelete.addEventListener("click", () => {
        options.onok();
        this._close(confirmEl);
      });

      btnCancel.addEventListener("click", () => {
        options.oncancel();
        this._close(confirmEl)
      });

      btnClose.addEventListener("click", () => {
        options.oncancel();
        this._close(confirmEl)
      });

     /*[btnCancel, btnClose].forEach(el => {
          el.addEventlistener("click", () => {
              options.oncancel();
              this._close(confirmEl);
            });
      });*/

      document.body.appendChild(template.content);

    },

   
    _close(confirmEl) {
      confirmEl.classList.add("confirm--close");
      confirmEl.addEventListener("animationend", () => {
        document.body.removeChild(confirmEl);
      });

    }
  };