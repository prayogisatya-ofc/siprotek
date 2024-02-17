Vue.createApp({
    data() {
        return {
            form: {
                uuid: '',
                first_name: '',
                last_name: '',
                telp: '',
                major: '',
                npm: '',
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

        var select2 = $('.select2')
        if (select2.length) {
            select2.each(function () {
                var $this = $(this);
                $this.wrap('<div class="position-relative"></div>').select2({
                    dropdownParent: $this.parent(),
                    placeholder: $this.data('placeholder')
                })
            })
        }
        $('.select2').on('change', (event) => {
            this.form.major = event.target.value
        })
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

            await axios.get(`/tutors/${this.form.uuid}/get-data`)
                .then((result) => {
                    $.unblockUI()
                    var data = result.data
                    this.form.first_name = data.first_name
                    this.form.last_name = data.last_name
                    this.form.npm = data.npm
                    this.form.telp = data.telp.replace('62', '')
                    this.form.major = data.major
                    this.form.status = data.status
                    $('.select2').val(data.major).trigger('change')
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

            await axios.post(`/tutors/${this.form.uuid}/submit`, this.form, { 
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
                    location.href = "/members"
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