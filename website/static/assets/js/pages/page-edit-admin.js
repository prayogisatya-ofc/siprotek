Vue.createApp({
    data() {
        return {
            form: {
                uuid: '',
                first_name: '',
                last_name: '',
                username: '',
                password: '',
                status: null
            },
            csrf: token,
            showPassword: false,
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        const currentUrl = window.location.href
        const urlPats = currentUrl.split('/')
        this.form.uuid = urlPats[urlPats.length - 1]

        this.getDetail()
    },
    methods: {
        async getDetail(){
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

            await axios.get(`/admins/${this.form.uuid}/get-data`)
                .then((result) => {
                    $.unblockUI()
                    var data = result.data
                    this.form.first_name = data.first_name
                    this.form.last_name = data.last_name
                    this.form.username = data.username
                    this.form.status = data.status
                })
                .catch(() => {
                    $.unblockUI()
                    Swal.fire({
                        icon: "warning",
                        text: error.response.data.error,
                        timer: 2000,
                        showConfirmButton: false,
                    })
                })
        },
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

            await axios.post(`/admins/${this.form.uuid}/submit`, this.form, { 
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
                    location.href = "/admins"
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
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        }
    },
    computed: {
        passwordFieldType() {
          return this.showPassword ? 'text' : 'password';
        },
        toggleButtonIcon() {
            return this.showPassword ? 'ti-eye' : 'ti-eye-off';
        }
    }
}).mount('#app')