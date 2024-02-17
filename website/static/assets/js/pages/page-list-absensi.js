Vue.createApp({
    data() {
        return {
            start_date: '',
            end_date: '',
            division: '',
            datas: [],
            pagination: {},
            csrf: token,
            modal: null,
            form: {
                division: null,
                note: null
            }
        }
    },
    delimiters: ['[[', ']]'],
    mounted(){
        this.modal = new bootstrap.Modal(document.getElementById('modalAdd'), {})
        this.initializeSelect2()
        this.initializeSelect22()
        this.getDatas(1)
    },
    methods: {
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
                this.division = event.target.value
                this.getDatas(1)
            })
        },
        initializeSelect22(){
            var select2 = $('.select2-2')
            if (select2.length) {
                select2.each(function () {
                    var $this = $(this);
                    $this.wrap('<div class="position-relative"></div>').select2({
                        dropdownParent: $this.parent(),
                        placeholder: $this.data('placeholder')
                    })
                })
            }
            $('.select2-2').on('change', (event) => {
                this.form.division = event.target.value
            })
        },
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

            await axios.get(`/presences/get-data?page=${page}&start_date=${this.start_date}&end_date=${this.end_date}&division=${this.division}`)
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
        async deleteData(key, name, date){
            Swal.fire({
                icon: "warning",
                html: 'Yakin mau hapus absensi divisi <b>' + name + '</b> pada <b>' + date + '</b>?',
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

                    await axios.post('/presences/delete', {key: key}, { 
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
        async onAdd(){
            
        },
        closeModal(){
            this.modal.hide()
            this.form.division = null
            this.form.note = null
        },
        async onAdd(){
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

            await axios.post('/presences/add', this.form, { 
                headers: { "X-CSRFToken": this.csrf }
            })
            .then(response => {
                $.unblockUI()
                this.closeModal()
                Swal.fire({
                    icon: "success",
                    text: response.data.success,
                    timer: 2000,
                    showConfirmButton: false,
                }).then(() => {
                    location.href = '/presences/' + response.data.uuid
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
        },
    }
}).mount('#app')