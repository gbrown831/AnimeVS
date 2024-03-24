import { Component, Output, EventEmitter, OnInit  } from '@angular/core';
import axios from 'axios';
import {NgbCollapseModule} from '@ng-bootstrap/ng-bootstrap';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import {
  trigger,
  state,
  style,
  animate,
  transition,
} from '@angular/animations';


@Component({
  selector: 'app-battle',
  standalone: true,
  imports: [NgbCollapseModule],
  templateUrl: './battle.component.html',  
  styleUrl: './battle.component.css',
  animations: [
    trigger('fadeImage', [
      state('hasWon', style({
        opacity: 1,
      })),
      state('hasLost', style({
        opacity: 0.6,
      })),
      transition('hasWon => hasLost', [
        animate('1s')
      ]),
    ])
  ]
})

export class BattleComponent {
  /**
   * Changes the view from the battle screen to the home screen
   */
  @Output() setView = new EventEmitter<boolean>();

  /**
   * The image URLs of the left and right characters
   */
  leftURL!: string;
  rightURL!: string;

  /**
   * The character information stored in database for both characters
   */
  left_char: any = {};
  right_char: any = {};

  /**
   * 
   */
  leftVotes!: string | number;
  rightVotes!: string | number;

  /**
   * Shows if the user has voted for a character on the screen
   */
  hasVoted: boolean = false;


  left_percentage!: string;
  right_percentage!: string;

/**
 * Triggers the app to change the view of the screen
 * @param isHome boolean to decide whether to return to the home screen
 */
  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

  // Request for two random characters for users to choose from 
  // When the screen first renders
  ngOnInit() {
    this.getImages();
  }

  /**
   * Retrieves information of two random characters stored
   * in the Flask database
   */
  getImages() {
    axios.get('https://anime-versus-a63b2afeb899.herokuapp.com/')
    .then((res) => {
      console.log(res.data)
      this.leftURL = res.data.char1_url[0]
      this.rightURL = res.data.char2_url[0]
      this.left_char = res.data.char1;
      this.right_char = res.data.char2;

      this.hasVoted = false;
    })
    .catch((err) => console.log(err));
  }


  /**
   * Saves a user choice of a battle in the Flask database
   * @param id the character ID of the user selected (hidden from the user)
   */
  postVotes(id: string | number) {

    this.hasVoted = true;
    axios.post('https://anime-versus-a63b2afeb899.herokuapp.com/', {
      "char1_id": this.left_char.id,
      "char2_id": this.right_char.id,
      "winner": id
    })
    .then((res) => {

      /**
       * The id of the first character in the database must be
       * less than the id of the second character in the database.
       * So, this tracks whether the order of ID's were swapped
       * within the backend response 
       */

      if (res.data.switch) {
        this.leftVotes = (res.data.votes2 * 100) / (res.data.votes1 + res.data.votes2);
        this.rightVotes = (res.data.votes1 * 100) / (res.data.votes1 + res.data.votes2);
      } else {
        this.leftVotes = (res.data.votes1 * 100) / (res.data.votes1 + res.data.votes2);
        this.rightVotes = (res.data.votes2 * 100) / (res.data.votes1 + res.data.votes2);
      }

      //Displaying the percentages of votes on screen
      this.left_percentage = Math.floor((this.leftVotes / 100) * 80).toString() + 'vw';
      this.right_percentage = Math.floor((this.rightVotes / 100) * 80).toString() + 'vw';

      this.leftVotes = Math.floor(this.leftVotes).toString() + '%'
      this.rightVotes = Math.floor(this.rightVotes).toString() + '%'
    })
    .catch((err) => console.log(err));

    // Used for smooth transitioning
    setTimeout(() => {
      this.getImages();
    }, 3000);
  }
}
