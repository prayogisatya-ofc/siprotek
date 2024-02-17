Vue.createApp({
    data() {
        return {
            form: {
                current_pw: null,
                new_pw: null,
                confirm_pw: null,
            },
            csrf: token,
            showCurrentPassword: null,
            showNewPassword: null,
            showConfirmPassword: null
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.getDetail()
    },
    methods: {
        async onSubmit(){
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

            await axios.post(`/password/submit`, this.form, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI()
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    location.href = "/"
                })
            })
            .catch(error => {
                $.unblockUI()
                Swal.fire({
                    icon: "warning",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                })
            })
        }
    }
}).mount('#app')