Vue.createApp({
    data() {
        return {
            search: '',
            major: '',
            status: '',
            datas: [],
            pagination: {},
            csrf: token,
            fileSelected: null,
            modal: null
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
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
            this.major = event.target.value
            this.getDatas(1)
        })
        this.modal = new bootstrap.Modal(document.getElementById('modalImport'), {})

        this.getDatas(1)
    },
    methods: {
        async getDatas(page){
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

            await axios.get(`/members/get-data?page=${page}&search=${this.search}&major=${this.major}&status=${this.status}`)
                .then((result) => {
                    $.unblockUI();

                    var data = JSON.parse(result.data)
                    this.datas = data.data
                    this.pagination = data.pagination
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
        async deleteData(key, name){
            Swal.fire({
                icon: "warning",
                html: 'Yakin mau hapus anggota <b>' + name + '</b>?',
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

                    await axios.post('/members/delete', {key: key}, { 
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
                            this.getDatas(1)
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
        nextPage(){
            if(this.pagination.has_next){
                this.getDatas(this.pagination.current_page_number + 1)
            }
        },
        previousPage(){
            if(this.pagination.has_previous){
                this.getDatas(this.pagination.current_page_number - 1)
            }
        },
        onFileChange(event) {
            this.fileSelected = event.target.files[0]
        },
        async onImport(){
            this.modal.hide()

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

            await axios.postForm('/members/import', {file: this.fileSelected}, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI();
                this.fileSelected = null
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    this.getDatas(1)
                })
            })
            .catch(error => {
                $.unblockUI();
                this.fileSelected = null
                Swal.fire({
                    icon: "error",
                    text: error.response.data.error,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    this.getDatas(1)
                })
            })
        }
    }
}).mount('#app')