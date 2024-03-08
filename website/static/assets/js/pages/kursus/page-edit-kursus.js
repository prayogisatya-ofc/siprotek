Vue.createApp({
    data() {
        return {
            meetings: [],
            members: [],
            form: {
                title: null,
                division: null,
                description: '',
                thumbnail: null
            },
            uuid: null,
            previewImage: null,
            editor: null,
            csrf: token
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        const currentUrl = window.location.href
        const urlPats = currentUrl.split('/')
        this.uuid = urlPats[urlPats.length - 1]

        this.getDetail()
        this.initializeSelect2()
    },
    methods: {
        quillInitial(){
            this.editor = new Quill('#snow-editor', {
                bounds: '#snow-editor',
                placeholder: 'Isi deskripsi untuk menjelaskan tentang kursus...',
                modules: {
                  formula: true,
                  toolbar: '#snow-toolbar'
                },
                theme: 'snow'
            })
            this.editor.root.innerHTML = this.form.description
            this.editor.on('text-change', () => {
                this.form.description = this.editor.root.innerHTML
            });
        },
        initializeSelect2(){
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
                this.form.division = event.target.value
            })
        },
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

            await axios.get(`/courses/${this.uuid}/get-data`)
                .then(result => {
                    $.unblockUI()
                    var data = result.data
                    this.form.title = data.title
                    this.previewImage = data.thumbnail
                    this.form.division = data.division
                    this.form.description = data.description
                    this.meetings = data.meetings
                    this.members = data.members
                    $('.select2').val(data.division).trigger('change')
                    this.quillInitial()
                })
                .catch(() => {
                    $.unblockUI();
                    Swal.fire({
                        icon: "warning",
                        text: "Gagal mengambil data!",
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

            await axios.postForm(`/courses/${this.uuid}/update`, this.form, { 
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
                    this.getDetail()
                    this.form.thumbnail = null
                })
            })
            .catch(error => {
                $.unblockUI()
                Swal.fire({
                    icon: "error",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                })
            })
        },
        onFileChange(event) {
            this.form.thumbnail = event.target.files[0]
        },
        async deleteData(key, title){
            Swal.fire({
                icon: "warning",
                html: 'Yakin mau hapus materi <b>' + title + '</b>?',
                showCancelButton: true,
                confirmButtonText: "Yakin",
                cancelButtonText: "Batal",
                customClass: {
                    confirmButton: 'btn btn-primary me-2 waves-effect waves-light',
                    cancelButton: 'btn btn-label-secondary waves-effect waves-light'
                },
                buttonsStyling: false
            }).then( async (result) => {
                if (result.isConfirmed) {
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

                    await axios.post(`/courses/${this.uuid}/delete`, {key: key}, { 
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
                            this.getDetail()
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
            })
        },
    }
}).mount('#app')