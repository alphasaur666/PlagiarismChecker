import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FileUploader } from 'ng2-file-upload';
import {
  HttpClient,
  HttpEventType,
  HttpErrorResponse,
} from '@angular/common/http';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css'],
})
export class FileUploadComponent implements OnInit {
  uploadForm: FormGroup;
  baseUrl: string;
  public uploadProgresses: Array<number> = new Array<number>();
  public movingStatus: Array<number> = new Array<number>();
  public filesMessage: string;
  public showProgress = false;

  public uploader: FileUploader = new FileUploader({
    isHTML5: true,
  });

  title = 'File Upload';
  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    @Inject('BASE_URL') baseUrl: string
  ) {
    this.baseUrl = baseUrl;
    this.filesMessage = 'No files added...';
  }

  uploadSubmit() {

    if (this.uploader.queue.length === 0) {
      return;
    }

   this.uploader.queue.sort((a, b) => b.file.size - a.file.size);

    for (let i = 0; i < this.uploader.queue.length; i++) {
      const data = new FormData();
      const fileItem = this.uploader.queue[i]._file;
      data.append('file' + i, fileItem, fileItem.name);

      this.showProgress = true;
      this.http
        .post(this.baseUrl + 'upload', data, {
          reportProgress: true,
          observe: 'events',
        })
        .subscribe((event) => {
          if (event.type === HttpEventType.UploadProgress) {
            this.uploadProgresses[i] = Math.round(
              (100 * event.loaded) / event.total
            );
            this.movingStatus[i] = 2;
          } else if (event.type === HttpEventType.Response) {
            if (!event.status) {
              this.movingStatus[i] = 2;
            } else {
              if (event.status === 200) {
                this.movingStatus[i] = 1;
              }
            }
          }
        }),
        (err: HttpErrorResponse) => {
          if (err.error instanceof Error) {
            // A client-side or network error occurred.
            console.log('An error occurred:', err.error.message);
            this.movingStatus[i] = 0;
          } else {
            // Backend returns unsuccessful response codes such as 404, 500 etc.
            console.log('Backend returned status code: ', err.status);
            console.log('Response body:', err.error);
            this.movingStatus[i] = 0;
          }
        };
    }
  }

  uploadFile($event) {
    console.log($event.target.files[0]);
    this.showProgress = false;
  }

  ngOnInit() {
    this.uploadForm = this.fb.group({
      document: [null, Validators.compose([Validators.required])],
    });

  }
}
