Vue.createApp({
    data() {
        return {
            form: {
                first_name: '',
                last_name: '',
                telp: '',
                major: '',
                npm: '',
            },
            csrf: token,
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
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

            await axios.get(`/account/get-data`)
                .then((result) => {
                    $.unblockUI()
                    var data = result.data
                    this.form.first_name = data.first_name
                    this.form.last_name = data.last_name
                    this.form.npm = data.npm
                    this.form.telp = data.telp.replace('62', '')
                    this.form.major = data.major
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

            await axios.post(`/account/submit`, this.form, { 
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