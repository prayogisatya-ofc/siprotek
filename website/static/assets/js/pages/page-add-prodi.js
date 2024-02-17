Vue.createApp({
    data() {
        return {
            forms: [{}],
            csrf: token,
        }
    },
    delimiters: ['[[', ']]'],
    methods: {
        addForm(){
            this.forms.push({})
        },
        removeForm(index) {
            this.forms.splice(index, 1);
        },
        async onSubmit(){
            if(this.forms.length == 0){
                Swal.fire({
                    icon: "warning",
                    text: "Masukkan dulu datanya!",
                    timer: 2000,
                    showConfirmButton: false,
                })
            } else {
                $.blockUI({
                    message: '<div class="spinner-border text-white" role="status"></div>',
                    css: {
                      backgroundColor: 'transparent',
                      border: '0'
                    },
                    overlayCSS: {
                      opacity: 0.5
                    }
                })
    
                await axios.post('/majors/add/submit', this.forms, { 
                    headers: { "X-CSRFToken": this.csrf }
                })
                .then(response => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "success",
                        text: response.data.success,
                        timer: 2000,
                        showConfirmButton: false,
                    }).then(() => {
                        location.href = "/majors"
                    })
                })
                .catch(error => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "error",
                        text: error.response.data.error,
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
            }
        }
    }
}).mount('#app')